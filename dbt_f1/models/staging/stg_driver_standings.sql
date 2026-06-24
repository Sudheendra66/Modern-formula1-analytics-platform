select
    standing_id,
    driver_id,
    position,
    points,
    wins,
    season,
    round,
    _loaded_at,
    _source
from {{ source('f1_raw', 'DRIVER_STANDINGS') }}
where _fivetran_deleted = false