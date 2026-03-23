import duckdb
import os

def get_database_connection(database_path: str = "data/database/clinic_dwh.duckdb") -> duckdb.DuckDBPyConnection:
    directory_path = os.path.dirname(database_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    db_connection = duckdb.connect(database=database_path)
    return db_connection