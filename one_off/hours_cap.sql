insert into hour_reason(hour_reason, display_name, description) values
('cap', 'Hours cap', 'Hours cap related entries');

-- credit everyone who has an owner type that would accrue hours
insert into hour_log(email, amount, hour_reason, hour_date)
select
  hb.email,
  -LEAST(0, hb.balance + 2 * ot.work_requirement) as credit,
  'cap',
  NOW()
from hour_balance hb
join current_owner_type cot on hb.email = cot.email
join owner_type ot on ot.owner_type = cot.owner_type
where hb.balance < -2 * ot.work_requirement
and ot.work_requirement > 0;
