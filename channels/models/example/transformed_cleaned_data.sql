{{ config(materialized='table') }}

WITH base_data AS (
    SELECT 
        "Channel Title",
        "Channel Username",
        "Message ID",
        COALESCE(NULLIF("Message Text", ''), 'No Message') AS message_text,  -- Handle empty strings as well
        CASE 
            WHEN "Date" = 'Unknown Date' THEN NULL
            WHEN REGEXP_LIKE("Date", '^\d{2} \w{3,9} \d{4}$') THEN TO_DATE("Date", 'DD Month YYYY')  -- Validate date format before converting
            ELSE NULL
        END AS message_date,
        "Media Path"
    FROM public.cleaned_data
),

filtered_data AS (
    SELECT 
        *
    FROM base_data
    WHERE message_text IS NOT NULL 
)

SELECT 
    "Channel Title",
    "Channel Username",
    "Message ID",
    message_text,
    message_date,
    "Media Path",
    CASE
        WHEN LENGTH(message_text) > 50 THEN 'Long Message'
        WHEN LENGTH(message_text) BETWEEN 1 AND 50 THEN 'Short Message'
        ELSE 'No Message'  -- Categorize based on message length
    END AS message_length_category
FROM filtered_data
ORDER BY message_date DESC  -- Order by message date
