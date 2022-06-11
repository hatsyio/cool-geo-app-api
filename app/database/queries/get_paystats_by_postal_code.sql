with selected_postal_codes as (
    select id, code
    from postal_codes
    where code = 28005
)
select *
from paystats
where id = (select id from selected_postal_codes)
;
