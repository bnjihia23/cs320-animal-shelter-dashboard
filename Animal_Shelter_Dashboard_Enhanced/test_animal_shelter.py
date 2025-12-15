# Quick database test
import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd

# Load env variables
load_dotenv()


def main():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

        print("Connected successfully!")

        # Check total rows
        df_count = pd.read_sql("SELECT COUNT(*) AS total FROM animals;", conn)
        print("Total rows:", df_count.iloc[0]['total'])

        # Show first 5 rows
        df_head = pd.read_sql("SELECT * FROM animals LIMIT 5;", conn)
        print("\nSample rows:")
        print(df_head)

        # Distinct animal types
        df_types = pd.read_sql("SELECT DISTINCT animal_type FROM animals ORDER BY animal_type;", conn)
        print("\nDistinct animal types:")
        print(df_types['animal_type'].to_list())

        conn.close()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
