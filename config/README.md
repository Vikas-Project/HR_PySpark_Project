# HR Employee 360 - PySpark Project

## Overview

An end-to-end HR data engineering project using PostgreSQL and PySpark.

The project extracts employee data from PostgreSQL, performs data quality checks and transformations using PySpark, creates an Employee 360 dataset, and writes the final result to Parquet.

## Technology Stack

- Python
- PySpark
- PostgreSQL
- Spark JDBC
- SQL
- Parquet
- Jupyter Notebook

## Project Structure

```text
HR_PySpark_Project/
│
├── notebooks/
│   └── hr_employee_360.ipynb
│
├── config/
│   ├── __init__.py
│   └── database_config.py
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── load_csv.py
│   ├── transform.py
│   ├── quality_checks.py
│   └── load.py
│
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_insert_sample_data.sql
│
├── output/
│   └── employee_360/
│
├── .gitignore
├── .env.example
├── requirements.txt
└── README.md
Database
The project uses PostgreSQL with the following tables:

departments
employees
job_roles
performance
salary
Data Pipeline
PostgreSQL
    |
    v
Spark JDBC
    |
    v
Data Quality Checks
    |
    v
Data Cleaning
    |
    v
Data Transformation
    |
    v
Employee 360
    |
    v
Parquet
Configuration
Database credentials are stored outside the project using Windows environment variables.
Required variables:
PGHOST
PGPORT
PGDATABASE
PGUSER
PGPASSWORD
Credentials must never be committed to GitHub.
## Loading source data from CSV
Create a `data\csv` folder in the project root and place one UTF-8 CSV file in it for each PostgreSQL table:

| File | Required header columns, in this order |
|---|---|
| `departments.csv` | `department_id,department_name,location,head_of_department` |
| `job_roles.csv` | `job_id,job_title,grade,minimum_salary,maximum_salary` |
| `employees.csv` | `employee_id,first_name,last_name,gender,dob,department_id,job_id,manager_id,hire_date,employment_type,status` |
| `performance.csv` | `performance_id,employee_id,review_year,goal_score,kpi_score,manager_rating,overall_rating,performance_category,promotion_recommended` |
| `salary.csv` | `employee_id,basic_salary,bonus,allowance,deductions,net_salary` |

Use `YYYY-MM-DD` for dates and `true` or `false` for `promotion_recommended`. Leave nullable values blank. The employee CSV can list managers after their reports; the loader resolves manager references after loading employees.

Create the schema and tables once by running `sql/01_create_tables.sql` in PostgreSQL. From the project root, replace the existing table data by running:

```powershell
python -m src.load_csv --confirm
```

For CSV files in a different folder, pass its path:

```powershell
python -m src.load_csv --csv-dir "C:\path\to\csv" --confirm
```

This command deletes the existing rows in all five HR tables and imports the CSV files as one transaction. If validation or insertion fails, PostgreSQL rolls back the replacement and preserves the previous data. The command requires `--confirm` to avoid accidental deletion.
Running the Project
Install dependencies:
pip install -r requirements.txt
Start Jupyter:
jupyter notebook
Open:
notebooks/hr_employee_360.ipynb
Run the notebook to execute the Employee 360 pipeline.
Output
The final Employee 360 dataset is written in Parquet format under:
output/employee_360/
Business Metrics
The project calculates:

Total compensation
Salary status
Salary validation
Employee age
Years of service
Performance metrics
Promotion eligibility
