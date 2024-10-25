SELECT
    city_name,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    AVG(cloud_cover) AS avg_cloud_cover
FROM
    weather_data.cloud_cover_data
WHERE
    EXTRACT(YEAR FROM date) = 2020
GROUP BY
    city_name,
    EXTRACT(YEAR FROM date),
    EXTRACT(MONTH FROM date)
ORDER BY
    city_name,
    year,
    month;