**Animal Shelter Dashboard Enhanced**



This project is a Python Dash web application for exploring animal

outcome data from the Austin Animal Center. It loads shelter records

into a MySQL database and provides an interactive dashboard to filter

results, view summary statistics, and visualize trends.



**Project Structure**



\-   app.py – Dash application and layout

\-   animal\_shelter.py – CRUD data access layer for the animals table

\-   load\_animals.py – One-time ETL script to load aac\_shelter\_outcomes.csv into MySQL

\-   aac\_shelter\_outcomes.csv – Source dataset

\-   assets/ – Static assets

\-   test\_animal\_shelter.py – test script to validate database connection



**Prerequisites**



Python 3.10+ and MySQL. 



Install dependencies:

pip install dash dash-leaflet pandas plotly mysql-connector-python python-dotenv



**Database Setup**



1. Create a MySQL database (default name in code is animalshelter).
2. Create a non-root MySQL user with access to that database.
3. Add a .env file or edit the existing one with appropriate values for your environment:

MYSQL\_HOST=localhost 

MYSQL\_PORT=3306 

MYSQL\_USER=your\_user

MYSQL\_PASSWORD=your\_password 

MYSQL\_DB=animalshelter



**Load Data**



python load\_animals.py



**Run Dashboard**



python app.py



Visit http://127.0.0.1:8050/





