import pandas as pd
import pyarrow as pa


def is_datetime(data):
    return pd.api.types.is_datetime64_any_dtype(data)


def is_numeric(data):
    return pd.api.types.is_any_real_numeric_dtype(data)


def map_df_schema(destination, origin):
    """
    From the origin data schema, it ensure the destination schema follows the appropriate schema.

    Parameters
    ----------
    destination: destination dataset
    origin: origin dataset

    Returns
    -------

    """
    if isinstance(destination, pd.DataFrame):
        destination = pa.Schema.from_pandas(destination, preserve_index=False)

    if isinstance(origin, pd.DataFrame):
        origin = pa.Schema.from_pandas(origin, preserve_index=False)

    mapped_schemas = []
    for col in destination:
        destination_field = destination.field(col.name).type
        try:
            origin_field = origin.field(col.name).type
            if destination_field != origin_field:
                mapped_schemas.append(pa.field(col.name, origin_field))
            else:
                mapped_schemas.append(pa.field(col.name, destination_field))
        except Exception as e:
            print("This is a new column that isn't present in the origin")
            mapped_schemas.append(pa.field(col.name, destination_field))

    return mapped_schemas
