import csv
import random
import os
import json
from faker import Faker
from datetime import datetime, timedelta
from dagster import asset


def initialize_faker_instance() -> Faker:
    faker_instance = Faker('vi_VN')
    Faker.seed(42)
    return faker_instance

def create_doctor_records(total_doctors: int) -> list:
    faker_instance = initialize_faker_instance()
    available_specialties = [
        "Nội Tim mạch", "Ngoại Thần kinh", "Nhi khoa", 
        "Sản phụ khoa", "Tai Mũi Họng", "Da liễu"
    ]

    doctor_records_list = []

    for doctor_index in range(1, total_doctors + 1):
        doctor_id = f"DOC_{doctor_index:03d}"
        doctor_name = faker_instance.name()

        assigned_specialty = random.choice(available_specialties)

        is_active_status = random.random() < 0.9

        doctor_record = {
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "specialty": assigned_specialty,
            "is_active": is_active_status
        }
        doctor_records_list.append(doctor_record)

    return doctor_records_list

def export_data_to_csv_file(data_records: list, output_file_path: str) -> None:
    directory_path = os.path.dirname(output_file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    csv_headers = ["doctor_id", "doctor_name", "specialty", "is_active"]

    with open(output_file_path, mode='w', encoding='utf-8', newline='') as target_file:
        csv_writer = csv.DictWriter(target_file, fieldnames=csv_headers)
        csv_writer.writeheader()
        csv_writer.writerows(data_records)

def generate_doctor_csv(file_path: str = "data/raw_files/doctors_lookup.csv", num_doctors: int = 15) -> None:
    generated_records = create_doctor_records(total_doctors=num_doctors)
    export_data_to_csv_file(data_records=generated_records, output_file_path=file_path)
    print(f"[THÀNH CÔNG] Đã tạo file danh mục bác sĩ tại: {file_path}")

def create_webhook_events(total_events: int) -> list:
    faker_instance = initialize_faker_instance()
    available_statuses = ["Chờ khám", "Hoàn thành", "Bị hủy"]

    webhook_events_list = []
    current_time = datetime.now()

    for event_index in range(1, total_events + 1):
        appointment_id = f"APT_{event_index:05d}"
        assigned_doctor_id = f"DOC_{random.randint(1, 15):03d}"

        random_days_ago = random.randint(0, 7)
        created_timestamp = current_time - timedelta(days=random_days_ago)

        patient_info_dict = {
            "patient_id": f"PAT_{faker_instance.unique.random_int(min=1000, max=9999)}",
            "patient_name": faker_instance.name(),
            "phone_number": faker_instance.phone_number()
        }

        base_event_record = {
            "appointment_id": appointment_id,
            "doctor_id": assigned_doctor_id,
            "patient_info": patient_info_dict,
            "status": random.choice(available_statuses),
            "created_at": created_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": created_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

        webhook_events_list.append(base_event_record)

        is_duplicate_event = random.random() < 0.1
        if is_duplicate_event:
            duplicate_record = base_event_record.copy()
            delayed_timestamp = created_timestamp + timedelta(minutes=random.randint(5, 60))
            duplicate_record["updated_at"] = delayed_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            duplicate_record["status"] = "Bị hủy"

            webhook_events_list.append(duplicate_record)

    random.shuffle(webhook_events_list)
    return webhook_events_list

def export_events_to_json(data_records: list, output_file_path: str) -> None:
    directory_path = os.path.dirname(output_file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(output_file_path, mode='w', encoding='utf-8') as target_file:
        json.dump(data_records, target_file, ensure_ascii=False, indent=4)

def generate_webhook_json(file_path: str = "data/raw_files/webhook_appointments.json", num_events: int = 50) -> None:
    generated_events = create_webhook_events(total_events=num_events)
    export_events_to_json(data_records=generated_events, output_file_path=file_path)
    print(f"[THÀNH CÔNG] Đã tạo file Webhook JSON ({len(generated_events)} sự kiện) tại: {file_path}")

if __name__ == "__main__":
    print("--- BẮT ĐẦU QUÁ TRÌNH SINH DỮ LIỆU ---")
    generate_doctor_csv()
    generate_webhook_json()
    print("--- HOÀN TẤT ---")

@asset(group_name="data_generation", compute_kind="python")
def generated_doctor_csv_file():
    """Asset: Đại diện cho file CSV nhân sự được tạo ra trên ổ cứng."""
    generate_doctor_csv()
    # Trả về đường dẫn để Dagster ghi nhận Metadata (tùy chọn)
    return "data/raw_files/doctors_lookup.csv"

@asset(group_name="data_generation", compute_kind="python")
def generated_webhook_json_file():
    """Asset: Đại diện cho file JSON Webhook được tạo ra trên ổ cứng."""
    generate_webhook_json()
    return "data/raw_files/webhook_appointments.json"