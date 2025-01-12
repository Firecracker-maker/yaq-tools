import logging
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

import yaqtools as yaqt

SECTORS = ["consumer-cyclical", "technology", "energy", "financial-services"]
logging.basicConfig(level=logging.INFO)


class DataLake:
    def __init__(
        self,
        root,
        end_date,
        dataset,
        start_date=None,
        qc=False,
        save=False,
        forensics=False,
    ):
        self.root = root
        self.end_date = end_date
        self.dataset = dataset
        self.qc = qc
        # the program can run for one date or a time series.
        self.start_date = start_date if start_date else end_date
        self.forensics = forensics
        self.save = save

        self.store = yaqt.StoreBackend()

        for directory in ["output", "forensics"]:
            dir_name = self.get_folders(directory)
            logging.info(f"Setting directory {dir_name}")
            os.makedirs(dir_name, exist_ok=True)
            setattr(self, directory + "_dir", dir_name)

    def get_folders(self, option):
        return os.path.join(self.root, self.dataset, option)

    def get_date_list(self):
        return pd.bdate_range(self.start_date, self.end_date)

    @staticmethod
    def get_sectors():
        return yaqt.get_sector_tickers(SECTORS)

    def get_price(self, tickers):
        data = yf.download(
            tickers,
            start=yaqt.datetime_to_str(self.start_date),
            end=yaqt.datetime_to_str(self.end_date),
        )
        df = data.stack(future_stack=True).reset_index()
        df.columns = [i for i in df.columns.values]
        # lower columns to make it cleaner and easier so we know we manipulate cols accordingly
        df.columns = [col.lower() for col in df.columns]
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        # Import to sort to ensure the shift performed later is inline with expectations.
        df.sort_index(ascending=True, inplace=True)

        return df

    def write_forensics_data(self, df, result_col, output_file):
        """
        Write Forensics data
        Parameters
        ----------
        df
        result_col
        output_file

        Returns
        -------

        """
        if self.save:
            df_failed = df.copy()
            df_failed = df_failed[~df_failed[result_col]]
            failed_delta_lake = os.path.join(self.forensics_dir, output_file)
            if not os.path.exists(failed_delta_lake):
                logging.info(f"The Deltalake does not exists yet {failed_delta_lake}")
                self.store.create(failed_delta_lake, date_column="date")

            if not df_failed.empty:
                self.store.write(
                    failed_delta_lake,
                    df_failed,
                    mode="overwrite",
                    schema_mode="overwrite",
                )
            else:
                logging.info(f"There are not data to write: {df_failed.shape}")
        else:
            logging.info(f"Save parameter is: {self.save}")

    def store_data(self, df, output_file):
        if self.save:
            delta_lake = os.path.join(self.output_dir, output_file)
            if not os.path.exists(delta_lake):
                self.store.create(delta_lake, date_column="date")

            if not df.empty:
                self.store.write(
                    delta_lake, df, mode="overwrite", schema_mode="overwrite"
                )
            else:
                logging.info(f"There are not data to write: {df.shape}")
        else:
            logging.info(f"Save parameter is: {self.save}")

    def check_missing_tckrs(self, df):
        # Data consistency
        # find tickers where we don't have any price
        def all_col_empty(grp):
            cols = grp.columns[grp.isna().any()].tolist()
            if len(cols) == 0:
                return None
            else:
                return ", ".join(cols)

        df_grp = (
            df.groupby("ticker").apply(lambda grp: all_col_empty(grp)).reset_index()
        )
        empty_tickers = df_grp[df_grp[0].notnull()]["ticker"].tolist()
        df["ticker_has_sufficient_info_result"] = ~df["ticker"].isin(empty_tickers)

        if self.forensics:
            self.write_forensics_data(
                df, "ticker_has_sufficient_info_result", "missing_tckrs"
            )

        df = df[df["ticker_has_sufficient_info_result"]]

        logging.info(f"The shape after QC 'missing_tckrs' is: {df.shape}")

        return df

    def check_close_consistence(self, df):
        # QC on Close price
        df["close_is_in_range_test"] = "close >= low and close <= high"
        df["close_is_in_range_columns"] = "close, low, high"

        # We must round here bc the close price and low price can have diff of units after 12 decimales.
        df["close_is_in_range_result"] = (
            df["close"].round(5) >= df["low"].round(5)
        ) & (df["close"].round(5) <= df["high"].round(5))

        if self.forensics:
            self.write_forensics_data(df, "close_is_in_range_result", "close_range")

        df = df[df["close_is_in_range_result"]]

        logging.info(f"The shape after QC 'close_range' is: {df.shape}")

        return df

    def check_sma(self, df, window=60):
        if "close_shift" not in df.columns:
            df["close_shift"] = df.groupby("ticker")["close"].shift(1)
            df["close_shift"].fillna(df["close"], inplace=True)

        df["simple_moving_avg"] = df.groupby("ticker")["close"].transform(
            lambda d: d.rolling(window, min_periods=1).mean()
        )
        df["simple_moving_std"] = df.groupby("ticker")["close"].transform(
            lambda d: d.rolling(window, min_periods=1).std()
        )
        df["simple_zscore"] = (df["close"] - df["simple_moving_avg"]) / df[
            "simple_moving_std"
        ]
        df["simple_zscore_test"] = "simple_zscore within abs(3)"
        df[
            "simple_zscore_columns"
        ] = "close, simple_moving_avg, simple_moving_std, simple_zscore"
        df["simple_zscore_result"] = (df["simple_zscore"] > -3) & (
            df["simple_zscore"] < 3
        )

        if self.forensics:
            self.write_forensics_data(df, "simple_zscore_result", "sma_zscore")

        df = df[df["simple_zscore_result"]]

        logging.info(
            f"The shape after QC 'simple moving average zscore' is: {df.shape}"
        )

        return df

    def check_ewm(self, df, window=60):
        if "close_shift" not in df.columns:
            df["close_shift"] = df.groupby("ticker")["close"].shift(1)
            df["close_shift"].fillna(df["close"], inplace=True)

        df["exp_moving_avg"] = df.groupby("ticker")["close"].transform(
            lambda d: d.ewm(span=window).mean()
        )
        df["exp_moving_std"] = df.groupby("ticker")["close"].transform(
            lambda d: d.ewm(span=window).std()
        )
        df["exp_zscore"] = (df["close"] - df["exp_moving_avg"]) / df["exp_moving_std"]
        df["exp_zscore_test"] = "exp_zscore within abs(3)"
        df["exp_zscore_columns"] = "close, exp_zscore_avg, exp_zscore_std, exp_zscore"
        df["exp_zscore_result"] = (df["exp_zscore"] > -3) & (df["exp_zscore"] < 3)

        if self.forensics:
            self.write_forensics_data(df, "exp_zscore_result", "ewm_zscore")

        df = df[df["exp_zscore_result"]]

        logging.info(f"The shape after QC 'exp moving average zscore' is: {df.shape}")

        return df

    def load_eq_prices(self, tickers):
        df = self.get_price(tickers)

        if self.qc:
            logging.info(f"The shape Before Any QC is applied is : {df.shape}")
            df = self.check_missing_tckrs(df)
            df = self.check_close_consistence(df)
            df = self.check_sma(df)
            df = self.check_ewm(df)

        if self.save:
            logging.info(f"The shape before saving is: {df.shape}")
            self.store_data(df, "data")

    def load_data(self):
        df_sectors = self.get_sectors()
        tickers = df_sectors.index.tolist()

        if self.dataset == "eq_prices":
            self.load_eq_prices(tickers)
        else:
            raise ValueError(f"dataset {self.dataset} is not implemented")

        print("This is completed")


if __name__ == "__main__":
    delta_directory = os.path.join("tmp", "datalake")
    data = DataLake(
        root=delta_directory,
        end_date=datetime(2025, 1, 3),
        dataset="eq_prices",
        start_date=datetime(2020, 1, 1),
        qc=True,
        save=True,
        forensics=True,
    )

    data.load_data()
