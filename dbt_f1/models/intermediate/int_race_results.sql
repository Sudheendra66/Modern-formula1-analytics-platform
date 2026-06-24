select

    r.result_id,

    r.driver_id,

    d.driver_name,

    ra.race_name,

    ra.country,

    r.season,

    r.round,

    r.position,

    r.points,

    {{ finish_category('r.position') }} as finish_category,

    r.grid,

    r.laps,

    r.status

from {{ ref('stg_results') }} r

left join {{ ref('stg_drivers') }} d
    on r.driver_id = d.driver_id

left join {{ ref('stg_races') }} ra
    on r.season = ra.season
   and r.round = ra.round