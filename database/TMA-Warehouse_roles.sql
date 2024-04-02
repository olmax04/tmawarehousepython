CREATE ROLE Employee;
CREATE ROLE Coordinator;
CREATE ROLE Admin;

GRANT SELECT, INSERT ON Requests TO Employee;
GRANT SELECT ON Items TO Employee;

GRANT SELECT, INSERT, UPDATE, DELETE ON Items TO Coordinator;
GRANT UPDATE, SELECT ON Requests TO Coordinator;
GRANT SELECT ON RequestsRows TO Coordinator;
GRANT SELECT ON RequestsRowsConnect TO Coordinator;

GRANT CONTROL TO Admin;

CREATE USER Employee FOR LOGIN Employee WITH PASSWORD = 'EmployeePass';
EXEC sp_addrolemember 'Employee', 'EmployeeUser';

CREATE USER Coordinator FOR LOGIN Coordinator WITH PASSWORD = 'CoordinatorPass';
EXEC sp_addrolemember 'Coordinator', 'CoordinatorUser';

CREATE USER AdminUser FOR LOGIN Admin WITH PASSWORD = 'CoordinatorPass';
EXEC sp_addrolemember 'Admin', 'AdminUser';
