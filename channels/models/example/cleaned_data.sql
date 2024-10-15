{{ config(materialized='table') }}

SELECT *
FROM public.cleaned_data
