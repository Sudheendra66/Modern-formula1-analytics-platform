WITH driver_scores AS (

    SELECT
        DRIVER_ID,
        DRIVER_NAME,
        TOTAL_RACES,
        WINS,
        PODIUMS,
        CAREER_POINTS,
        AVG_FINISH_POSITION,

        ROUND((WINS * 100.0) / NULLIF(TOTAL_RACES, 0), 2) AS WIN_RATE,
        ROUND((PODIUMS * 100.0) / NULLIF(TOTAL_RACES, 0), 2) AS PODIUM_RATE

    FROM {{ ref('mart_driver_performance') }}

    -- Minimum eligibility criteria for GOAT ranking
    WHERE DRIVER_NAME IS NOT NULL
      AND TOTAL_RACES >= 50
      AND CAREER_POINTS >= 300

),

goat_scores AS (

    SELECT
        *,

        ROUND(
              (CAREER_POINTS / NULLIF(MAX(CAREER_POINTS) OVER (), 0)) * 35
            + (WINS / NULLIF(MAX(WINS) OVER (), 0)) * 25
            + (PODIUMS / NULLIF(MAX(PODIUMS) OVER (), 0)) * 20
            + (WIN_RATE / 100) * 10
            + (PODIUM_RATE / 100) * 10,
            2
        ) AS GOAT_SCORE

    FROM driver_scores

)

SELECT
    *,
    DENSE_RANK() OVER (ORDER BY GOAT_SCORE DESC) AS GOAT_RANK

FROM goat_scores