create database security_app;
use security_app;
create table users (
id int auto_increment primary key,
name varchar (100) not null,
email varchar (250) not null unique,
password varchar (255) not null
);
select * from users
CREATE TABLE password_checks (
id INT auto_increment primary key,
user_email varchar(255),
password_strength varchar (20),
score int,
created_at timestamp default current_timestamp
);
CREATE TABLE email_checks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    result VARCHAR(50),
    score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE url_checks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    result VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);