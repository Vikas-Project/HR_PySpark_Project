import os

def get_database_config():
    """
    Read PostgreSQL connection details from environment variables.
    """

    required_variables = [
        "PGHOST",
        "PGPORT",
        "PGDATABASE",
        "PGUSER",
        "PGPASSWORD",
    ]

    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise EnvironmentError(
            "Missing required environment variables: "
            + ", ".join(missing_variables)
        )

    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT")
    database = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")

    jdbc_url = (
        f"jdbc:postgresql://{host}:{port}/{database}"
    )

    connection_properties = {
        "user": user,
        "password": password,
        "driver": "org.postgresql.Driver",
    }

    return {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "jdbc_url": jdbc_url,
        "connection_properties": connection_properties,
    }

if __name__ == "__main__":
    try:
        config = get_database_config()

        print("PostgreSQL configuration loaded successfully!")
        print("Host:", config["host"])
        print("Port:", config["port"])
        print("Database:", config["database"])
        print("User:", config["user"])
        print("JDBC URL:", config["jdbc_url"])

    except Exception as e:
        print("Configuration error:")
        print(e)