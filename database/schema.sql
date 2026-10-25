-- Employee Management System
-- Restored Edition (2026)
-- Reconstructed from the original 2021 project

CREATE DATABASE IF NOT EXISTS EmpManagement;

USE EmpManagement;

-- Main employee records
CREATE TABLE IF NOT EXISTS employee (
    empid INT PRIMARY KEY,
    empname VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Not Paid',
    bonus VARCHAR(100) DEFAULT 'None',
    contact VARCHAR(20)
);

-- Employee authentication
CREATE TABLE IF NOT EXISTS employee_login (
    empid INT PRIMARY KEY,
    pin_salt VARCHAR(32) NOT NULL,
    pin_hash VARCHAR(64) NOT NULL,

    CONSTRAINT fk_employee_login
        FOREIGN KEY (empid)
        REFERENCES employee(empid)
        ON DELETE CASCADE
);
