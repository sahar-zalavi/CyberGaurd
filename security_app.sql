create database security_app;
use security_app;
create table users (
id int auto_increment primary key,
name varchar (100) not null,
email varchar (250) not null unique,
password varchar (255) not null
);
select * from users
