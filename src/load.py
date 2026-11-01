def write_parquet(df, output_path, mode="overwrite"):
    """
    Write DataFrame to Parquet.
    """

    (
        df.write
        .mode(mode)
        .parquet(output_path)
    )


def read_parquet(spark, output_path):
    """
    Read Employee 360 Parquet output.
    """

    return spark.read.parquet(output_path)


def show_parquet(spark, output_path, num_rows=5, truncate=False):
    """
    Read Parquet output, display rows, and return the DataFrame.
    """

    df = read_parquet(spark, output_path)
    df.show(num_rows, truncate=truncate)
    return df
