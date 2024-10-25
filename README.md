# Data Engineering Exercise Solution

## Objective

The goal of this project is to design and implement a Python script to fetch hourly cloud cover data for London, Amsterdam, and Lisbon from the [Open-Meteo API](https://open-meteo.com/). The data includes timestamps and fields for cloud cover metrics (`cloud_cover`, `cloud_cover_low`, `cloud_cover_mid`, and `cloud_cover_high`) for all timestamps between 2012 and 2022. This data is then stored in a PostgreSQL database for further analysis using SQL.

## Technical Requirements

- **Programming Languages:** Python and SQL
- **Database:** PostgreSQL (local installation or Docker container)
- **Data Source:** Open-Meteo API
- **Data Schema:** Star schema (dimension and fact tables)
- **Libraries:** `requests`, `psycopg2`, `pandas`, etc.
- **Analysis Query:** Calculate average cloud cover by city and month-year for the year 2020 only.
- **Version Control:** GitHub repository with all code and a `README.md` file explaining the solution.
- **GUI Application:** Use a GUI application like DBeaver for querying and visualizing PostgreSQL data.

## Steps

### 1. Setting Up Your Environment

1. **Installing Required Software:**
   - Python
   - PostgreSQL (or use a Docker container)
   - DBeaver (GUI for PostgreSQL)

2. **Creating a New GitHub Repository:**
   - Initialize a new repository for this project and push your code.

### 2. Running PostgreSQL Using Docker

To run PostgreSQL in a Docker container:

```bash
# Pull the PostgreSQL Docker image
docker pull postgres

# Run the PostgreSQL container
docker run --name postgres -e POSTGRES_USER=yourusername -e POSTGRES_PASSWORD=yourpassword -d -p 5432:5432 postgres
```


### 3. Connecting to PostgreSQL via DBeaver

1. **Open DBeaver.**
2. **Create a New Database Connection:**
   - Select PostgreSQL from the list of databases.
   - Enter the following connection details:
     - **Host:** `localhost`
     - **Port:** `5432`
     - **Database:** `postgres` (or your database name)
     - **Username:** `postgres`
     - **Password:** `yourpassword` (the password you set in the Docker command)

3. **Test the Connection:**
   - Click the "Test Connection" button to ensure that everything is working.

### 4. Create Database Tables

Create two tables in your PostgreSQL database following the Kimball star schema design:

- **cities** (Dimension Table)
- **cloud_cover_data** (Fact Table)
 

### 5. Running the Project

- Creating a Python script that performs the following:
  - Fetches hourly cloud cover data from the Open-Meteo API.
  - Stores the data in the PostgreSQL database.
  
To run the project, execute the following command in your terminal:

```bash
python ingestion.py --config_path path/to/your/config.yaml
```

### 6. Analyzing the Data

You can query the `Cloud_cover_report` view in DBeaver.

Creating a SQL view named `Cloud_cover_report` that calculates the average cloud cover for each city, month, and year in 2020:


## Conclusion

This project demonstrates the ability to design and implement a data pipeline that fetches, processes, and stores data from an API into a relational database. The resulting data can be queried and analyzed using SQL, providing insights into cloud cover patterns in selected cities over time.