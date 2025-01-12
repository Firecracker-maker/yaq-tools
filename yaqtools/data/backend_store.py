"""
Module to write in DeltaLake.
"""
import getpass
import os
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Any, List, Literal, Tuple, Union

import pandas as pd
import pyarrow as pa
from deltalake import CommitProperties, DeltaTable, write_deltalake


def init_metadata(
    date_column: str = None, pd_idx_column: List[str] = None, tz: str = "UTC"
):
    metadata = {
        "creation_timestamp": datetime.now().isoformat(),
        "creation_user": getpass.getuser(),
        "update_timestamp": datetime.now().isoformat(),
        "update_user": getpass.getuser(),
        "date_column": date_column if date_column else "",
        "pd_index_columns": ",".join([col for col in pd_idx_column])
        if pd_idx_column
        else "",
        "tz": tz,
    }

    return metadata


class StoreBackend:
    @staticmethod
    def path_exist(path):
        return os.path.exists(path)

    def delete(self, path):
        if self.path_exist(path):
            shutil.rmtree(path, ignore_errors=False)
        else:
            print("Nothing to delete")

    @staticmethod
    def build_commit_properties(custom_metadata):
        return CommitProperties(custom_metadata=custom_metadata)

    def create(
        self,
        path: Path,
        date_column: str = None,
        pd_idx_column: List[str] = None,
        tz: str = "UTC",
        force_dt: bool = False,
    ):
        if DeltaTable.is_deltatable(str(path)) and not force_dt:
            return

        metadata = init_metadata(date_column, pd_idx_column, tz)

        try:
            # create an Empty DeltaTable
            DeltaTable.create(
                table_uri=path,
                schema=pa.schema(
                    [
                        pa.field("empty", pa.string()),
                        pa.field("empty_binary", pa.binary(-1)),
                    ]
                ),
                custom_metadata=metadata,
            )

        except Exception as err:
            print(err)

            if force_dt:
                self.delete(path)
                DeltaTable.create(table_uri=path, custom_metadata=metadata)

    def write(
        self,
        path: Path,
        data: Union[pd.DataFrame, pd.Series, pa.Table],
        schema: pa.Schema = None,
        partition_by: Union[List[str], str] = None,
        mode: Literal["error", "append", "overwrite", "ignore"] = "error",
        schema_mode: Literal["merge", "overwrite"] = None,
        predicate: str = None,
        commit_properties: Union[dict, CommitProperties] = None,
    ):
        if not isinstance(data, (pd.DataFrame, pd.Series)):
            raise NotImplementedError("This is not yet implemented")

        if isinstance(commit_properties, dict):
            commit_properties = self.build_commit_properties(commit_properties)

        if not DeltaTable.is_deltatable(str(path)):
            raise ValueError("The path provided is not a real Deltalake location")

        if isinstance(data, (pd.DataFrame, pd.Series)):
            data = pa.Table.from_pandas(df=data, preserve_index=False)

        # I only want to support RUST because the predicate for overwrite mode are only available in RUST
        write_deltalake(
            table_or_uri=path,
            data=data,
            schema=schema,
            partition_by=partition_by,
            mode=mode,
            engine="rust",
            schema_mode=schema_mode,
            predicate=predicate,
            commit_properties=commit_properties,
        )

    def delete_records(
        self,
        path: Path,
        predicate: str,
        commit_properties: Union[dict, CommitProperties] = None,
    ):
        if isinstance(commit_properties, dict):
            commit_properties = self.build_commit_properties(commit_properties)

        dt = DeltaTable(path)
        dt.delete(predicate=predicate, commit_properties=commit_properties)

    def read(
        self,
        path: Path,
        version: int = None,
        columns: List[str] = None,
        filters: Tuple[str, str, Any] = None,
        date_column: str = None,
        start_date: Union[datetime, date, str] = None,
        end_date: Union[datetime, date, str] = None,
    ):
        """

        Parameters
        ----------
        path: Path where the deltalake is located
        version: version to load using "time travel" feature in DeltaLake"
        columns: column to return when loading the data
        filters: Filters to filter the data on when loading. Format should follow:
                    [(col1, ">=", 1), (col1, "<", 5)]
        date_column: Date column for end-users to programmatically filter their data using StoreBackEnd
                    built-in functions. It can be combined with "non-date" filters
        start_date: Start date to use for filtering
        end_date: end date to use for filtering

        Returns
        -------

        """
        if not DeltaTable.is_deltatable(str(path)):
            raise ValueError("The path provided is not a real Deltalake location")

        dt = DeltaTable(path, version=version)

        if date_column:
            filters = filters if filters else []
            filters.append(
                [(date_column, ">=", start_date), (date_column, "<", end_date)]
            )

        df = dt.to_pandas(columns, filters)

        return df
