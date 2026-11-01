from pyspark.sql.window import Window

from pyspark.sql.functions import (
    col,
    trim,
    initcap,
    row_number,
    desc,
    when,
    floor,
    datediff,
    current_date,
)


def clean_employees(employees_df):

    return (
        employees_df
        .filter(col("employee_id").isNotNull())
        .dropDuplicates(["employee_id"])
        .withColumn(
            "first_name",
            initcap(trim(col("first_name")))
        )
        .withColumn(
            "last_name",
            initcap(trim(col("last_name")))
        )
    )


def clean_salary(salary_df):

    return (
        salary_df
        .filter(col("employee_id").isNotNull())
        .dropDuplicates(["employee_id"])
    )


def get_latest_performance(performance_df):

    performance_window = (
        Window
        .partitionBy("employee_id")
        .orderBy(desc("review_year"))
    )

    return (
        performance_df
        .withColumn(
            "row_num",
            row_number().over(performance_window)
        )
        .filter(col("row_num") == 1)
        .drop("row_num")
    )


def create_employee_360(data):

    employees = clean_employees(data["employees"])
    salary = clean_salary(data["salary"])
    performance = get_latest_performance(
        data["performance"]
    )

    departments = data["departments"]
    job_roles = data["job_roles"]

    employee_department = (
        employees.alias("e")
        .join(
            departments.alias("d"),
            col("e.department_id")
            == col("d.department_id"),
            "left",
        )
    )

    employee_job = (
        employee_department
        .join(
            job_roles.alias("j"),
            col("e.job_id")
            == col("j.job_id"),
            "left",
        )
    )

    employee_salary = (
        employee_job
        .join(
            salary.alias("s"),
            col("e.employee_id")
            == col("s.employee_id"),
            "left",
        )
    )

    employee_performance = (
        employee_salary
        .join(
            performance.alias("p"),
            col("e.employee_id")
            == col("p.employee_id"),
            "left",
        )
    )

    employee_360 = employee_performance.select(

        col("e.employee_id").alias("employee_id"),

        col("e.first_name").alias("first_name"),
        col("e.last_name").alias("last_name"),
        col("e.gender").alias("gender"),
        col("e.dob").alias("date_of_birth"),

        col("d.department_name").alias("department"),
        col("d.location").alias("department_location"),

        col("j.job_title").alias("job_title"),
        col("j.grade").alias("job_grade"),
        col("j.minimum_salary").alias("minimum_salary"),
        col("j.maximum_salary").alias("maximum_salary"),

        col("e.manager_id").alias("manager_id"),
        col("e.hire_date").alias("hire_date"),
        col("e.employment_type").alias("employment_type"),
        col("e.status").alias("employee_status"),

        col("s.basic_salary").alias("basic_salary"),
        col("s.bonus").alias("bonus"),
        col("s.allowance").alias("allowance"),
        col("s.deductions").alias("deductions"),
        col("s.net_salary").alias("net_salary"),

        col("p.review_year").alias("review_year"),
        col("p.goal_score").alias("goal_score"),
        col("p.kpi_score").alias("kpi_score"),
        col("p.manager_rating").alias("manager_rating"),
        col("p.overall_rating").alias("overall_rating"),
        col("p.performance_category").alias(
            "performance_category"
        ),
        col("p.promotion_recommended").alias(
            "promotion_recommended"
        ),
    )

    return employee_360


def add_business_metrics(employee_360):

    employee_360 = employee_360.withColumn(
        "salary_status",
        when(
            col("basic_salary") < col("minimum_salary"),
            "Below Range",
        )
        .when(
            col("basic_salary") > col("maximum_salary"),
            "Above Range",
        )
        .otherwise("Within Range"),
    )

    employee_360 = employee_360.withColumn(
        "total_compensation",
        (
            col("basic_salary")
            + col("bonus")
            + col("allowance")
        ),
    )

    employee_360 = employee_360.withColumn(
        "calculated_net_salary",
        (
            col("basic_salary")
            + col("bonus")
            + col("allowance")
            - col("deductions")
        ),
    )

    employee_360 = employee_360.withColumn(
        "salary_validation",
        when(
            col("net_salary")
            == col("calculated_net_salary"),
            "Valid",
        ).otherwise("Mismatch"),
    )

    employee_360 = employee_360.withColumn(
        "promotion_status",
        when(
            (
                col("overall_rating") >= 4.10
            )
            & (
                col("promotion_recommended") == True
            ),
            "Eligible",
        )
        .when(
            col("overall_rating") >= 4,
            "Review",
        )
        .otherwise("Not Eligible"),
    )

    employee_360 = employee_360.withColumn(
        "age",
        floor(
            datediff(
                current_date(),
                col("date_of_birth"),
            ) / 365.25
        ),
    )

    employee_360 = employee_360.withColumn(
        "years_of_service",
        floor(
            datediff(
                current_date(),
                col("hire_date"),
            ) / 365.25
        ),
    )

    return employee_360
