import os
from typing import Dict, List, Any, Optional

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AnimalShelter:
    # CRUD interface for the animals table in the MySQL animalshelter database.
    def __init__(self):
        # Read connection settings from .env
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DB", "animalshelter")

    # Internal helper
    def _get_connection(self):
        # Open a new MySQL connection
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    # Create
    def create(self, data: Dict[str, Any]) -> bool:
        # Insert a new record into animals.
        if not data:
            return False

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            columns = list(data.keys())
            values = list(data.values())

            column_list = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(values))

            sql = f"INSERT INTO animals ({column_list}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Create Error: {e}")
            return False

    # Read
    def read(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # Fetch records from animals that match simple equality filters.

        results: List[Dict[str, Any]] = []

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Select all useful columns
            base_sql = """
                SELECT
                    id,
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
                FROM animals
            """

            params: List[Any] = []
            where_clauses: List[str] = []

            if query:
                for key, value in query.items():
                    if value is None:
                        continue
                    where_clauses.append(f"{key} = %s")
                    params.append(value)

            if where_clauses:
                base_sql += " WHERE " + " AND ".join(where_clauses)

            cursor.execute(base_sql, params)

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            for row in rows:
                row_dict = dict(zip(columns, row))
                results.append(row_dict)

            cursor.close()
            conn.close()

        except Error as e:
            print(f"Read Error: {e}")
            return []

        return results

    # Update
    def update(self, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        # Update rows matching query with new_values
        if not query or not new_values:
            return 0

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            set_clauses = []
            params: List[Any] = []
            for key, value in new_values.items():
                set_clauses.append(f"{key} = %s")
                params.append(value)

            where_clauses = []
            for key, value in query.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)

            sql = f"UPDATE animals SET {', '.join(set_clauses)}"
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)

            cursor.execute(sql, params)
            conn.commit()

            modified = cursor.rowcount

            cursor.close()
            conn.close()
            return modified

        except Error as e:
            print(f"Update Error: {e}")
            return 0

    # Delete
    def delete(self, query: Dict[str, Any]) -> int:
        # Delete rows matching `query`.
        if not query:
            return 0

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            where_clauses = []
            params: List[Any] = []

            for key, value in query.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)

            sql = "DELETE FROM animals"
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)

            cursor.execute(sql, params)
            conn.commit()

            deleted = cursor.rowcount

            cursor.close()
            conn.close()
            return deleted

        except Error as e:
            print(f"Delete Error: {e}")
            return 0
