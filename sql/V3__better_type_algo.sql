create or replace view current_owner_type as
select
  distinct
  email,
first_value(owner_type) over (partition by email order by start_date desc)
    as owner_type
from owner_owner_type where start_date < CURRENT_DATE;
