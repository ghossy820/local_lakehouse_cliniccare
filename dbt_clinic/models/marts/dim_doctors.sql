WITH staging_doctors AS (
    SELECT * FROM {{ ref('stg_doctors') }}
),

final_dimension AS (
    SELECT
        doctor_id,
        doctor_name,
        specialty,
        is_active
    FROM staging_doctors
)

SELECT * FROM final_dimension