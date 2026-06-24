select

    driver_id,

    driver_name,

    count(*) as total_races,

    sum(case when position = 1 then 1 else 0 end) as wins,

    sum(case when position <= 3 then 1 else 0 end) as podiums,

    sum(points) as career_points,

    round(avg(position),2) as avg_finish_position,

    round(
        (
            sum(case when position = 1 then 1 else 0 end) * 100.0
        ) / nullif(count(*),0),
        2
    ) as win_rate,

    round(
        (
            sum(case when position <= 3 then 1 else 0 end) * 100.0
        ) / nullif(count(*),0),
        2
    ) as podium_rate

from {{ ref('int_race_results') }}

group by
    driver_id,
    driver_name