{% snapshot driver_standings_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='standing_id',
        strategy='check',
        check_cols=['position','points','wins']
    )
}}

select *
from {{ ref('stg_driver_standings') }}

{% endsnapshot %}