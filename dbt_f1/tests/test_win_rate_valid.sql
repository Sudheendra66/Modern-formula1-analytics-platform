select *
from {{ ref('mart_driver_analytics') }}
where win_rate > 100
or win_rate < 0