WITH source_data AS (
    SELECT * FROM {{ source('raw_layer', 'raw_appointments') }}
),

extracted_data AS (
    SELECT
        appointment_id,
        doctor_id,
        patient_info.patient_id AS patient_id,
        patient_info.patient_name AS patient_name,
        patient_info.phone_number AS phone_number,
        status,
        CAST(created_at AS TIMESTAMP) AS created_at,
        CAST(updated_at AS TIMESTAMP) AS updated_at
    FROM source_data
),

deduplicated_data AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY appointment_id 
            ORDER BY updated_at DESC
        ) AS row_num
    FROM extracted_data
),

final_data AS (
    SELECT
        appointment_id,
        doctor_id,
        patient_id,
        patient_name,
        phone_number,
        status,
        created_at,
        updated_at
    FROM deduplicated_data
    WHERE row_num = 1
)

SELECT * FROM final_data