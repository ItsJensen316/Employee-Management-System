-- Employee Management System
-- Sample Data for Restored Edition (2026)

USE EmpManagement;

INSERT INTO employee
    (empid, empname, department, salary, status, bonus, contact)
VALUES
    (1001, 'Alex Morgan', 'Office', 45000.00, 'Paid', 'None', '0500001001'),
    (1002, 'Jordan Lee', 'Sales', 38000.00, 'Paid', 'None', '0500001002'),
    (1003, 'Taylor Smith', 'Accounts', 52000.00, 'Not Paid', 'None', '0500001003'),
    (1004, 'Casey Brown', 'Security', 32000.00, 'Paid', 'None', '0500001004'),
    (1005, 'Riley Wilson', 'Transport', 35000.00, 'Paid', 'None', '0500001005'),
    (1006, 'Avery Davis', 'Maintenance', 40000.00, 'Not Paid', 'None', '0500001006'),
    (1007, 'Jamie Taylor', 'Cleaning', 28000.00, 'Paid', 'None', '0500001007')
ON DUPLICATE KEY UPDATE empid = empid;
