{{ config(materialized='table') }}

WITH cleaned_data AS (
    -- Selecting all columns from the cleaned_data table using the source reference
    SELECT 
        *,
        CAST("Message ID" AS INTEGER) AS cleaned_message_id,  -- Convert Message ID to integer
        UPPER("Channel Username") AS standardized_channel_name  -- Standardize channel name to uppercase
    FROM {{ source('channels', 'cleaned_data') }}  -- Correctly reference the source table
)

SELECT 
    "Channel Title",
    standardized_channel_name AS "Channel Username",  -- Use the CTE column
    cleaned_message_id AS "Message ID",  -- Use the CTE column
    "Message Text",
    "Date",
    "Media Path"
FROM cleaned_data;  -- This references the CTE defined above
