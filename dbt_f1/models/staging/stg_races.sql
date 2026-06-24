select
    race_id,
    race_name,
    circuit_id,
    circuit_name,
    locality,
    country,
    season,
    round,
    date,
    time,
    url,
    _loaded_at,
    _source
from {{ source('f1_raw', 'RACES') }}
where _fivetran_deleted = false