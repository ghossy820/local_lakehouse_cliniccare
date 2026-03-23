WITH source_data AS (
       SELECT * FROM {{ source('raw_layer', 'raw_doctors') }}
),

casted_data AS (
    SELECT
        CAST(doctor_id AS VARCHAR) AS doctor_id,
        CAST(doctor_name AS VARCHAR) AS doctor_name,
        CAST(specialty AS VARCHAR) AS specialty,
        CAST(is_active AS BOOLEAN) AS is_active
    FROM source_data
)

SELECT * FROM casted_data