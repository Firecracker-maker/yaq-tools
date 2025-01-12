from yaqtools.core import df_utils


def to_sql_filters(df, keys):
    """
    Convert a dataframe to a list of "sql like filters"
    Parameters
    ----------
    df
    keys

    Returns
    -------

    """
    filters = []
    for col in keys:
        if df_utils.is_datetime(df[col]):
            unique_values = df[col].unique().tolist()
            data = "','".join([v.strftime("%Y%m%d") for v in unique_values])
            filters.append(f"{col} in ('{data}')")
        if df_utils.is_numeric(df[col]):
            unique_values = df[col].unique().tolist()
            data = ",".join([str(num) for num in unique_values])
            filters.append(f"{col} in ({data})")
        else:
            unique_values = df[col].unique().tolist()
            data = "','".join(unique_values)
            filters.append(f"{col} in ('{data}')")

    return filters
