{{ config(materialized='table') }}

WITH base_data AS (
    SELECT 
        "Channel Title" AS channel_title,  -- Rename to follow naming conventions
        "Channel Username" AS channel_username,
        "Message ID" AS message_id,
        COALESCE(NULLIF("Message Text", ''), 'No Message') AS message_text,  -- Handle empty strings as well
        CASE 
            WHEN "Date" = 'Unknown Date' THEN NULL
            WHEN "Date" SIMILAR TO '%## %% %####' THEN TO_TIMESTAMP("Date", 'DD Month YYYY')  -- Handle date with pattern
            ELSE NULL
        END AS message_date,
        "Media Path" AS media_path
    FROM public.cleaned_data
),

filtered_data AS (
    SELECT 
        *
    FROM base_data
    WHERE message_text IS NOT NULL 
)

SELECT 
    channel_title,  -- Use renamed columns for consistency
    channel_username,
    message_id,
    message_text,
    message_date,
    media_path,
    CASE
        WHEN LENGTH(message_text) > 50 THEN 'Long Message'
        WHEN LENGTH(message_text) BETWEEN 1 AND 50 THEN 'Short Message'
        ELSE 'No Message'  -- Categorize based on message length
    END AS message_length_category
FROM filtered_data
ORDER BY message_date DESC
