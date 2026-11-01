from config.database_config import get_database_config


TABLES = [
    "departments",
    "employees",
    "job_roles",
    "performance",
    "salary",
]


def read_table(spark, table_name):
    """
    Read a PostgreSQL table using Spark JDBC.
    """

    config = get_database_config()

    return spark.read.jdbc(
        url=config["jdbc_url"],
        table=f"hr_data.{table_name}",
        properties=config["connection_properties"],
    )


def extract_all_tables(spark):
    """
    Extract all HR tables from PostgreSQL.
    """

    data = {}

    for table in TABLES:
        data[table] = read_table(spark, table)

    return data
