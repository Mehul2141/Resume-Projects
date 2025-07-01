CREATE DATABASE user_details;
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'Dhruv@#123';
GRANT ALL ON user_details.* TO 'newuser'@'localhost';