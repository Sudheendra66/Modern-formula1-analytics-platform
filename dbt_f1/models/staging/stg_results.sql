select
    result_id,
    driver_id,
    constructor_id,
    season,
    round,
    position,
    points,
    grid,
    laps,
    status,
    _loaded_at,
    _source
from {{ source('f1_raw', 'RESULTS') }}
where _fivetran_deleted = false