-- CREATING SCHEMA FOR WEATHER DATA
CREATE SCHEMA IF NOT EXISTS weather_data;

-- CREATING TABLE CITIES
CREATE TABLE weather_data.cities (
    city_name VARCHAR(100) primary key,
    latitude FLOAT,
    longitude FLOAT
);