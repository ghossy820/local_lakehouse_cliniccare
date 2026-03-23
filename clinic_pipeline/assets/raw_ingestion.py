from clinic_pipeline.resources.db_connection import get_database_connection
from dagster import asset

def load_json_to_raw(json_file_path: str = "data/raw_files/webhook_appointments.json") -> None:
    db_connection = get_database_connection()
    
    sql_query = f"""
        CREATE OR REPLACE TABLE raw_appointments AS 
        SELECT * FROM read_json_auto('{json_file_path}');
    """
    db_connection.execute(sql_query)
    db_connection.close()
    print(f"[THÀNH CÔNG] Đã nạp dữ liệu JSON vào bảng: raw_appointments")

def load_csv_to_raw(csv_file_path: str = "data/raw_files/doctors_lookup.csv") -> None:
    db_connection = get_database_connection()
    
    sql_query = f"""
        CREATE OR REPLACE TABLE raw_doctors AS 
        SELECT * FROM read_csv_auto('{csv_file_path}');
    """
    db_connection.execute(sql_query)
    db_connection.close()
    print(f"[THÀNH CÔNG] Đã nạp dữ liệu CSV vào bảng: raw_doctors")

def run_raw_ingestion() -> None:
    load_csv_to_raw()
    load_json_to_raw()

if __name__ == "__main__":
    print("--- BẮT ĐẦU NẠP DỮ LIỆU THÔ VÀO DUCKDB ---")
    run_raw_ingestion()
    print("--- HOÀN TẤT ---")

@asset(
    group_name="raw_layer", 
    deps=["generated_doctor_csv_file"], 
    compute_kind="duckdb"
)
def raw_doctors_table():
    """Asset: Bảng raw_doctors trong DuckDB (Phụ thuộc vào file CSV)."""
    load_csv_to_raw()

@asset(
    group_name="raw_layer", 
    deps=["generated_webhook_json_file"], 
    compute_kind="duckdb"
)
def raw_appointments_table():
    """Asset: Bảng raw_appointments trong DuckDB (Phụ thuộc vào file JSON)."""
    load_json_to_raw()