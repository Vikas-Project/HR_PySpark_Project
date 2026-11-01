from pyspark.sql.functions import col, sum


def check_duplicate_keys(df, key_column):
    """
    Return duplicate key values.
    """

    return (
        df.groupBy(key_column)
        .count()
        .filter(col("count") > 1)
    )


def check_null_counts(df):
    """
    Return NULL counts for every column.
    """

    return df.select(
        [
            sum(
                col(column).isNull().cast("int")
            ).alias(column)
            for column in df.columns
        ]
    )


def run_quality_checks(data):
    """
    Run basic quality checks against source datasets.
    """

    results = {}

    results["employee_duplicates"] = check_duplicate_keys(
        data["employees"],
        "employee_id",
    )

    results["salary_duplicates"] = check_duplicate_keys(
        data["salary"],
        "employee_id",
    )

    results["performance_duplicates"] = check_duplicate_keys(
        data["performance"],
        "performance_id",
    )

    return results
