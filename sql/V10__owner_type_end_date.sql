create or replace view current_owner_type as
with valid_owner_type as (
select email,
       owner_type,
       start_date
from owner_owner_type where end_date is null or end_date > CURRENT_DATE
)
select
  distinct
  email,
  first_value(owner_type) over (partition by email order by start_date desc)
    as owner_type
from valid_owner_type where start_date < CURRENT_DATE;
