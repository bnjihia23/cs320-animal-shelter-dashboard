# One-time data loading script for AAC animal shelter CSV file.
import os
from typing import List

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# Helper functions
def get_db_connection():
    # Create and return a MySQL connection using values from .env.

    load_dotenv()

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DB", "animalshelter"),
    )


def create_animals_table(cursor) -> None:
    # Create the animals table if it does not already exist.

    create_sql = """
    CREATE TABLE IF NOT EXISTS animals (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        age_upon_outcome TEXT,
        animal_id VARCHAR(30),
        animal_type VARCHAR(50),
        breed VARCHAR(255),
        color VARCHAR(255),
        date_of_birth DATETIME,
        datetime DATETIME,
        monthyear VARCHAR(20),
        name VARCHAR(100),
        outcome_subtype VARCHAR(100),
        outcome_type VARCHAR(30),
        sex_upon_outcome VARCHAR(50),
        location_lat DOUBLE,
        location_long DOUBLE,
        age_upon_outcome_in_weeks DOUBLE
    );
    """
    cursor.execute(create_sql)


def load_csv(path: str, limit: int = 10_000) -> pd.DataFrame:
    # Load the CSV into a Pandas DataFrame.

    df = pd.read_csv(path)

    if limit is not None:
        df = df.head(limit)

    # Normalize column names to exactly match our table schema
    expected_cols: List[str] = [
        "age_upon_outcome",
        "animal_id",
        "animal_type",
        "breed",
        "color",
        "date_of_birth",
        "datetime",
        "monthyear",
        "name",
        "outcome_subtype",
        "outcome_type",
        "sex_upon_outcome",
        "location_lat",
        "location_long",
        "age_upon_outcome_in_weeks",
    ]
    df = df[expected_cols]

    return df


def insert_animals(df: pd.DataFrame) -> None:
    # Insert all rows from `df` into the animals table.

    conn = get_db_connection()
    cursor = conn.cursor()

    create_animals_table(cursor)

    # Clear any existing data so the table stays in a known state.
    cursor.execute("DELETE FROM animals;")

    insert_sql = """
        INSERT INTO animals (
            age_upon_outcome,
            animal_id,
            animal_type,
            breed,
            color,
            date_of_birth,
            datetime,
            monthyear,
            name,
            outcome_subtype,
            outcome_type,
            sex_upon_outcome,
            location_lat,
            location_long,
            age_upon_outcome_in_weeks
        )
        VALUES (
            %(age_upon_outcome)s,
            %(animal_id)s,
            %(animal_type)s,
            %(breed)s,
            %(color)s,
            %(date_of_birth)s,
            %(datetime)s,
            %(monthyear)s,
            %(name)s,
            %(outcome_subtype)s,
            %(outcome_type)s,
            %(sex_upon_outcome)s,
            %(location_lat)s,
            %(location_long)s,
            %(age_upon_outcome_in_weeks)s
        );
    """

    records = df.to_dict(orient="records")
    print(f"Prepared {len(records)} rows with {len(df.columns)} columns each.")
    print("Inserting rows into MySQL...")

    cursor.executemany(insert_sql, records)
    conn.commit()

    print("Done.")
    cursor.close()
    conn.close()


# Script entry point
if __name__ == "__main__":
    CSV_PATH = "aac_shelter_outcomes.csv"

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Could not find {CSV_PATH}. "
            "Place the CSV in the same folder as load_animals.py."
        )

    df_animals = load_csv(CSV_PATH)
    insert_animals(df_animals)
