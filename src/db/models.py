from sqlalchemy import Column, Float, Integer, MetaData, Table, String

metadata_obj = MetaData()


measurement_table = Table(
    "measurement",
    metadata_obj,
    Column("time", Integer),
    Column("value", Float),
    Column("type", String),
    Column("created_at", Float),
)
