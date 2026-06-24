{% macro finish_category(position) %}

case
    when {{ position }} = 1 then 'Winner'
    when {{ position }} <= 3 then 'Podium'
    when {{ position }} <= 10 then 'Points Finish'
    else 'No Points'
end

{% endmacro %}