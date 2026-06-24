{{
    config(
        materialized='incremental',
        unique_key='result_id'
    )
}}

select *
from {{ ref('int_race_results') }}

{% if is_incremental() %}

where _loaded_at >
(
    select max(_loaded_at)
    from {{ this }}
)

{% endif %}