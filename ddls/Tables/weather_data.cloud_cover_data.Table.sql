-- CREATING TABLE CLOUD COVER DATA
CREATE TABLE cloud_cover_data (
	city_name VARCHAR(100),
    date Timestamp,
    cloud_cover FLOAT,
    cloud_cover_low FLOAT,
    cloud_cover_mid FLOAT,
    cloud_cover_high FLOAT,
    PRIMARY KEY (city_name, date),
    FOREIGN KEY (city_name) REFERENCES cities(city_name)
);

