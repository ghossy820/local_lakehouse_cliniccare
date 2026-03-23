# clinic_pipeline/dashboard.py
import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Clinic Analytics", page_icon="🏥", layout="wide")
st.title("🏥 Bảng Điều Khiển Phòng Khám Tuan-Clinic")
st.markdown("---")

@st.cache_data
def load_data():
    conn = duckdb.connect("data/database/clinic_dwh.duckdb", read_only=True)
    
    query = """
        SELECT 
            f.appointment_id,
            f.patient_name,
            d.doctor_name,
            d.specialty,
            f.current_status,
            f.created_at
        FROM main.fact_appointments f
        LEFT JOIN main.dim_doctors d 
            ON f.doctor_id = d.doctor_id
        ORDER BY f.created_at DESC
    """
    df = conn.execute(query).df()
    conn.close()
    return df

df = load_data()

total_appointments = len(df)
completed = len(df[df['current_status'] == 'Hoàn thành'])
cancelled = len(df[df['current_status'] == 'Bị hủy'])

col1, col2, col3 = st.columns(3)
col1.metric(label="Tổng Lượt Đặt Khám", value=total_appointments)
col2.metric(label="Đã Hoàn Thành", value=completed)
col3.metric(label="Bị Hủy", value=cancelled)

st.markdown("---")

st.subheader("📋 Chi tiết Lịch khám")
st.dataframe(
    df, 
    use_container_width=True,
    hide_index=True
)