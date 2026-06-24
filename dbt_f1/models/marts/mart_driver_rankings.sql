select

    driver_id,
    driver_name,
    career_points,
    wins,
    podiums,
    total_races,
    avg_finish_position,
    win_rate,
    podium_rate,
    goat_score,
    goat_rank as driver_rank

from {{ ref('mart_driver_analytics') }}