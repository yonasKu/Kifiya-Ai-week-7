-- tests/test_message_date_is_valid.sql

SELECT *
FROM {{ ref('transformed_cleaned_data') }}
WHERE message_date IS NULL  -- Check for invalid dates
