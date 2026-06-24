select *
from {{ ref('mart_driver_analytics') }}
where goat_score < 0