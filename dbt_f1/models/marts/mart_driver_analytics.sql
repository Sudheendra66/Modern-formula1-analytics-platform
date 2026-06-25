SELECT
    perf.DRIVER_ID,
    perf.DRIVER_NAME,
    perf.TOTAL_RACES,
    perf.WINS,
    perf.PODIUMS,
    perf.CAREER_POINTS,
    perf.AVG_FINISH_POSITION,
    perf.WIN_RATE,
    perf.PODIUM_RATE,
    rankings.GOAT_SCORE,
    rankings.GOAT_RANK

FROM {{ ref('mart_driver_performance') }} perf
LEFT JOIN {{ ref('mart_driver_rankings') }} rankings
    ON perf.DRIVER_ID = rankings.DRIVER_ID
WHERE perf.DRIVER_NAME IS NOT NULL