WITH staging_appointments AS (
    SELECT * FROM {{ ref('stg_appointments') }}
),

dim_doctors AS (
    SELECT * FROM {{ ref('dim_doctors') }}
),

accumulating_fact AS (
    SELECT
        a.appointment_id,
        a.patient_id,
        a.patient_name,
        a.phone_number,
        
        COALESCE(d.doctor_id, 'UNKNOWN') AS doctor_id,
        
        a.status AS current_status,
        a.created_at,
        a.updated_at,
        
        CASE 
            WHEN a.status = 'Hoàn thành' THEN a.updated_at 
            ELSE NULL 
        END AS completed_at,
        
        CASE 
            WHEN a.status = 'Bị hủy' THEN a.updated_at 
            ELSE NULL 
        END AS cancelled_at

    FROM staging_appointments AS a

    LEFT JOIN dim_doctors AS d
        ON a.doctor_id = d.doctor_id
)

SELECT * FROM accumulating_fact