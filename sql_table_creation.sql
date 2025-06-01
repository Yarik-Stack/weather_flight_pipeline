
DROP DATABASE IF EXISTS sql_workshop ;
CREATE DATABASE sql_workshop;
USE sql_workshop;


CREATE TABLE  cities (
    city_id INT PRIMARY KEY, 
    city VARCHAR(255) NOT NULL
);


CREATE TABLE  city_info (
    city_id INT PRIMARY KEY,
    population INT,
    country VARCHAR(255) NOT NULL,
    date DATE, 
    FOREIGN KEY (city_id) REFERENCES cities(city_id) 
);


 SELECT * FROM cities;