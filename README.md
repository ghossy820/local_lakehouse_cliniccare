# 🏥 Clinic Data Pipeline (End-to-End)

Dự án xây dựng hệ thống xử lý dữ liệu tự động cho phòng khám, chuyển đổi từ dữ liệu thô (Webhook JSON & CSV) sang Data Warehouse chuẩn Star Schema để phục vụ báo cáo BI.

## 🚀 Kiến trúc Hệ thống (Tech Stack)
- **Language:** Python 3.10+
- **Orchestration:** Dagster (Software-Defined Assets)
- **Warehouse:** DuckDB (In-process OLAP)
- **Transformation:** dbt (Data Build Tool)
- **BI Dashboard:** Streamlit
- **Automation:** Makefile

## 🛠️ Chức năng chính
1. **Data Ingestion:** Tự động nạp dữ liệu từ Webhook (JSON) và Danh mục bác sĩ (CSV).
2. **Data Modeling:** Xây dựng Star Schema với các bảng Fact và Dimension.
3. **Quality Control:** Kiểm thử dữ liệu tự động (Unique, Not Null) bằng dbt tests.
4. **Monitoring:** Theo dõi Phả hệ dữ liệu (Data Lineage) trực quan trên giao diện Dagster.

## 🏃 Cách vận hành
1. Cài đặt môi trường: `make setup`
2. Khởi động hệ thống điều phối: `dagster dev`
3. Xem Dashboard báo cáo: `make dashboard`