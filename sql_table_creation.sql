DROP DATABASE IF EXISTS sql_workshop;
CREATE DATABASE sql_workshop;
USE sql_workshop;

-- Главная таблица с городами и погодой
CREATE TABLE cities (
    city_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(255) NOT NULL,
    longitude FLOAT,
    latitude FLOAT,
    temperature FLOAT,
    weather VARCHAR(100),
    description VARCHAR(255),
    airport_name VARCHAR(255),
    icao_code VARCHAR(10),
    iata_code VARCHAR(10),
    date DATE
);

CREATE TABLE city_info (
    info_id INT PRIMARY KEY AUTO_INCREMENT,
    city_id INT,
    population INT,
    country VARCHAR(255),
    date DATE
);

CREATE TABLE flights (
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    arrival_airport_icao VARCHAR(10),
    departure_airport_icao VARCHAR(10),
    scheduled_arrival_time DATETIME,
    flight_number VARCHAR(20),
    timestamp_flight DATETIME
);

SELECT * FROM cities LIMIT 5;
SELECT * FROM city_info LIMIT 5;
SELECT * FROM flights LIMIT 5;
