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
