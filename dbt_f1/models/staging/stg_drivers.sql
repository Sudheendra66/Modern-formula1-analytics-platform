select

    id as driver_id,
    name as driver_name,
    given_name,
    family_name,
    nationality,
    date_of_birth,
    url,

    _loaded_at,
    _source

from {{ source('f1_raw', 'DRIVERS') }}

where _fivetran_deleted = false