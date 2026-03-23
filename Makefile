export PYTHONPATH=.

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help setup generate clean

help:
	@echo "--- HỆ THỐNG ĐIỀU KHIỂN DỰ ÁN CLINIC DATA PIPELINE ---"
	@echo "Các lệnh có thể dùng:"
	@echo "  make setup      : Khởi tạo môi trường ảo và cài đặt thư viện"
	@echo "  make generate   : Chạy script sinh dữ liệu giả (CSV/JSON)"
	@echo "  make clean      : Dọn dẹp môi trường và dữ liệu thô"

setup:
	@echo "[HỆ THỐNG] Đang khởi tạo môi trường ảo tại $(VENV)..."
	python3 -m venv $(VENV)
	@echo "[HỆ THỐNG] Đang cài đặt thư viện từ requirements.txt..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "[THÀNH CÔNG] Môi trường đã sẵn sàng!"

generate:
	@echo "[HỆ THỐNG] Đang thực thi script sinh dữ liệu..."
	$(PYTHON) clinic_pipeline/assets/data_generators.py
	@echo "[THÀNH CÔNG] Dữ liệu đã được tạo trong data/raw_files/"

ingest:
	@echo "[HỆ THỐNG] Đang nạp dữ liệu thô vào DuckDB..."
	$(PYTHON) clinic_pipeline/assets/raw_ingestion.py
	@echo "[THÀNH CÔNG] Dữ liệu đã nằm gọn trong kho clinic_dwh.duckdb"

dashboard:
	@echo "[HỆ THỐNG] Đang khởi động BI Dashboard..."
	$(VENV)/bin/streamlit run clinic_pipeline/dashboard.py

clean:
	@echo "[CẢNH BÁO] Đang xóa môi trường ảo và dữ liệu tạm..."
	rm -rf $(VENV)
	rm -rf data/raw_files/*.csv
	rm -rf data/raw_files/*.json
	@echo "[XONG] Thư mục đã sạch sẽ."