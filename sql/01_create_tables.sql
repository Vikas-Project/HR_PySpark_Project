CREATE SCHEMA IF NOT EXISTS hr_data;

CREATE TABLE IF NOT EXISTS hr_data.departments (
    department_id VARCHAR(10) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    head_of_department VARCHAR(100),
);


CREATE TABLE IF NOT EXISTS hr_data.job_roles (
    job_id VARCHAR(10) PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    grade VARCHAR(20),
    minimum_salary NUMERIC(12,2),
    maximum_salary NUMERIC(12,2),

    CONSTRAINT chk_salary_range
    CHECK (minimum_salary <= maximum_salary)
);


CREATE TABLE IF NOT EXISTS hr_data.employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20),
    dob DATE,
    department_id VARCHAR(10),
    job_id VARCHAR(10),
    manager_id VARCHAR(10),
    hire_date DATE,
    employment_type VARCHAR(30),
    status VARCHAR(30),

    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES hr_data.departments(department_id),

    CONSTRAINT fk_employee_job
        FOREIGN KEY (job_id)
        REFERENCES hr_data.job_roles(job_id),

    CONSTRAINT fk_employee_manager
        FOREIGN KEY (manager_id)
        REFERENCES hr_data.employees(employee_id)
);


CREATE TABLE IF NOT EXISTS hr_data.performance (
    performance_id VARCHAR(10) PRIMARY KEY,
    employee_id VARCHAR(10) NOT NULL,
    review_year INTEGER NOT NULL,
    goal_score NUMERIC(5,2),
    kpi_score NUMERIC(5,2),
    manager_rating NUMERIC(5,2),
    overall_rating NUMERIC(5,2),
    performance_category VARCHAR(30),
    promotion_recommended BOOLEAN,

    CONSTRAINT fk_performance_employee
        FOREIGN KEY (employee_id)
        REFERENCES hr_data.employees(employee_id)
);


CREATE TABLE IF NOT EXISTS hr_data.salary (
    employee_id VARCHAR(10) PRIMARY KEY,
    basic_salary NUMERIC(12,2),
    bonus NUMERIC(12,2),
    allowance NUMERIC(12,2),
    deductions NUMERIC(12,2),
    net_salary NUMERIC(12,2),

    CONSTRAINT fk_salary_employee
        FOREIGN KEY (employee_id)
        REFERENCES hr_data.employees(employee_id)
);