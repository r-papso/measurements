from sqlalchemy import Column, Float, Integer, MetaData, Table, String

metadata_obj = MetaData()

# Table representing the database table. We do not introduce any keys / constraints / indexes in
# order to maximize write throughput.
measurement_table = Table(
    "measurement",
    metadata_obj,
    Column("time", Integer),
    Column("value", Float),
    Column("type", String),
    Column("created_at", Float),
)
