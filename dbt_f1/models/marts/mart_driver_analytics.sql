select

    driver_id,
    driver_name,

    total_races,
    wins,
    podiums,
    career_points,
    avg_finish_position,

    win_rate,
    podium_rate,

    round(
        (
            (win_rate * 0.4)
            +
            (podium_rate * 0.3)
            +
            (
                (career_points / nullif(total_races,0))
                * 0.3
            )
        ),
        2
    ) as goat_score,

    dense_rank() over (
        order by
        (
            (win_rate * 0.4)
            +
            (podium_rate * 0.3)
            +
            (
                (career_points / nullif(total_races,0))
                * 0.3
            )
        ) desc
    ) as goat_rank

from {{ ref('mart_driver_performance') }}
where driver_name is not null