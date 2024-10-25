
# Data Engineering Exercise

## Context
Clouds can significantly interfere with satellite signal reception. To ensure optimal performance of satellite-based services, it's essential to have accurate cloud cover data for potential locations.

## Objective
Design and implement a Python script to fetch hourly cloud cover data for London, Amsterdam, and Lisbon from the Open-Meteo API (https://open-meteo.com/). This should include a timestamp and the fields cloud_cover, cloud_cover_low, cloud_cover_mid, and cloud_cover_high for all timestamps between 2012 and 2022. Store this data in a PostgreSQL database, then analyze the data using SQL.

Not all information is provided in this document, because we also want to see that you are able to find this API and figure out how to interact with it.

## Technical Requirements
- **Programming Languages:** Python and SQL
- **Database:** PostgreSQL (local installation or Docker container)
- **Data Source:** Open-Meteo API
- **Data Schema:** Star schema (dimension and fact tables)
- **Analysis Query:** Calculate average cloud cover by city and month-year for the year 2020 only.
- **Version Control:** GitHub repository with all your code and a README.md file explaining the solution.
- **GUI Application:** Install a GUI application like DBeaver for querying and visualizing your PostgreSQL data.

## Steps
1. **Set up your environment:**
   - Install Python, PostgreSQL (or use a Docker container), and a GUI application like DBeaver.
   - Create a new GitHub repository for your project.
  
2. **Fetch data:**
   - Write a Python script to retrieve hourly cloud cover data from the Open-Meteo API (all fields mentioned in the objective section).

3. **Store data:**
   - Design the data schema based on a Kimball-like methodology (star schema), with dimension and fact tables (you should need at least one of each).
   - Use Python to fetch the data and to connect to your PostgreSQL database and insert the fetched data.

4. **Analyse data:**
   - Write a SQL query to calculate the average cloud cover (only need to use the field cloud_cover) for each city, month, and year in 2020.
   - Use DBeaver or a similar tool to execute your SQL query and visualize the results.

5. **Document your work:**
   - Create a README.md file in your GitHub repository explaining your project setup, code structure, and the analysis steps.

## Additional Considerations
- **Interview Follow-up:** Be prepared to discuss your approach to the exercise, including the design decisions you made, the libraries or tools you used, and any challenges you encountered. You may also be asked to explain specific parts of your code or to make a minor modification to your SQL query, such as restricting the analysis to a single year. Additionally, you may be asked questions such as "Based on the data you analyzed, for each month, which city would be the best location for a satellite receiver to have (on average) less cloud interference?"

## Deliverables
- Your GitHub repository containing the Python script, SQL statements, and the README.md file.

## Tips
- Feel free to use any Python libraries or tools you find helpful.
- Refer to the Open-Meteo API documentation for information on available data and API endpoints.
- You may use LLMs like ChatGPT or CoPilot, as well as online resources, friends, family, or mentors to assist you. We will only ask you to tell us where you needed help, so that we don’t ask you harder questions in that area.
- Don't hesitate to ask for help if you encounter any challenges.

We're looking forward to reviewing your solution and learning more about your data engineering skills.
