import argparse
import csv
from pathlib import Path

import psycopg2

from config.database_config import get_database_config


TABLE_COLUMNS = {
    "departments": (
        "department_id",
        "department_name",
        "location",
        "head_of_department",
    ),
    "job_roles": (
        "job_id",
        "job_title",
        "grade",
        "minimum_salary",
        "maximum_salary",
    ),
    "employees": (
        "employee_id",
        "first_name",
        "last_name",
        "gender",
        "dob",
        "department_id",
        "job_id",
        "manager_id",
        "hire_date",
        "employment_type",
        "status",
    ),
    "performance": (
        "performance_id",
        "employee_id",
        "review_year",
        "goal_score",
        "kpi_score",
        "manager_rating",
        "overall_rating",
        "performance_category",
        "promotion_recommended",
    ),
    "salary": (
        "employee_id",
        "basic_salary",
        "bonus",
        "allowance",
        "deductions",
        "net_salary",
    ),
}

TABLE_LOAD_ORDER = (
    "departments",
    "job_roles",
    "employees",
    "performance",
    "salary",
)

EMPLOYEE_COLUMNS_WITHOUT_MANAGER = tuple(
    column for column in TABLE_COLUMNS["employees"] if column != "manager_id"
)

DEFAULT_CSV_DIR = Path(__file__).resolve().parents[1] / "data" / "csv"


def validate_csv_files(csv_dir):
    """Check that every expected CSV exists and has the expected header."""
    csv_paths = {}

    for table_name in TABLE_LOAD_ORDER:
        csv_path = csv_dir / f"{table_name}.csv"
        if not csv_path.is_file():
            raise FileNotFoundError(f"Required CSV file was not found: {csv_path}")

        with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
            header = next(csv.reader(csv_file), None)

        if header != list(TABLE_COLUMNS[table_name]):
            expected = ", ".join(TABLE_COLUMNS[table_name])
            actual = ", ".join(header) if header else "(empty file)"
            raise ValueError(
                f"Invalid header in {csv_path}. "
                f"Expected: {expected}. Found: {actual}."
            )

        csv_paths[table_name] = csv_path

    return csv_paths


def _copy_csv(cursor, table_name, csv_file):
    columns = ", ".join(TABLE_COLUMNS[table_name])
    cursor.copy_expert(
        f"COPY hr_data.{table_name} ({columns}) "
        "FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '')",
        csv_file,
    )


def _load_employees(cursor, csv_file):
    cursor.execute(
        "CREATE TEMP TABLE employee_csv_stage "
        "(LIKE hr_data.employees) ON COMMIT DROP"
    )
    columns = ", ".join(TABLE_COLUMNS["employees"])
    cursor.copy_expert(
        f"COPY employee_csv_stage ({columns}) "
        "FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '')",
        csv_file,
    )

    target_columns = ", ".join(EMPLOYEE_COLUMNS_WITHOUT_MANAGER)
    select_columns = ", ".join(
        f"employee_csv_stage.{column}"
        for column in EMPLOYEE_COLUMNS_WITHOUT_MANAGER
    )
    cursor.execute(
        f"INSERT INTO hr_data.employees ({target_columns}) "
        f"SELECT {select_columns} FROM employee_csv_stage"
    )
    cursor.execute(
        "UPDATE hr_data.employees AS employee "
        "SET manager_id = employee_csv_stage.manager_id "
        "FROM employee_csv_stage "
        "WHERE employee.employee_id = employee_csv_stage.employee_id "
        "AND employee_csv_stage.manager_id IS NOT NULL"
    )


def load_csv_files(csv_dir):
    """Replace the HR tables with CSV data in one database transaction."""
    csv_paths = validate_csv_files(csv_dir)
    config = get_database_config()
    connection = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        dbname=config["database"],
        user=config["user"],
        password=config["connection_properties"]["password"],
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "TRUNCATE TABLE "
                    "hr_data.performance, "
                    "hr_data.salary, "
                    "hr_data.employees, "
                    "hr_data.job_roles, "
                    "hr_data.departments "
                    "RESTART IDENTITY"
                )

                for table_name in TABLE_LOAD_ORDER:
                    with csv_paths[table_name].open(
                        encoding="utf-8-sig",
                        newline="",
                    ) as csv_file:
                        if table_name == "employees":
                            _load_employees(cursor, csv_file)
                        else:
                            _copy_csv(cursor, table_name, csv_file)
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Replace all hr_data tables with data from the five CSV files. "
            "The replacement is transactional."
        )
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DEFAULT_CSV_DIR,
        help=f"Folder containing the CSV files (default: {DEFAULT_CSV_DIR})",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required confirmation that existing table data will be deleted.",
    )
    args = parser.parse_args()

    if not args.confirm:
        parser.error("this operation deletes existing table data; pass --confirm")

    load_csv_files(args.csv_dir)
    print("All HR tables were replaced successfully from the CSV files.")


if __name__ == "__main__":
    main()
