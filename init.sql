CREATE DATABASE IF NOT EXISTS task_database;
USE task_database;
GRANT ALL PRIVILEGES ON task_database.* TO 'taskuser'@'%';
FLUSH PRIVILEGES;
