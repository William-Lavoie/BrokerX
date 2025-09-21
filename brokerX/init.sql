-- Used to give permissions to the runner in the CI script
CREATE DATABASE IF NOT EXISTS test_brokerX_db;

CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON test_brokerX_db.* TO 'user'@'%';
FLUSH PRIVILEGES;
