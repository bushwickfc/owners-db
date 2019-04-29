create or replace view owner_view as
select
  o.pos_id,
  ot.owner_type,
  ot.display_name as owner_type_name,
  o.email,
  o.first_name,
  o.last_name,
  /* Name */
  concat(o.first_name, ' ', o.last_name,
  ' // ',
  /* Status code */
  CASE WHEN oe.owner_price is null then
  3
  else
  (NOT (oe.owner_price AND s.owner_price AND ot.owner_price))::int + 1
  end,
  ' // ',
  /* Hour balance */
  coalesce(h.balance, 0),
  /* Owner type code */
  ot.pos_display,
  /* Equity owed (if relevant) */
  oe.pos_display)
    as pos_display,
  coalesce(h.balance, 0) as hour_balance,
  oe.paid as equity_paid,
  oe.due as equity_due,
  least(oe.paid - oe.due, 0) as equity_delinquent,
  oe.owner_price as equity_current,
  s.owner_price as hours_current,
  (coalesce(oe.owner_price,false) AND s.owner_price AND ot.owner_price)
    as owner_price,
  - least(oe.paid - oe.due, 0) as equity_to_be_paid,
  oe.plan_join_date,
  oe.equity_type,
  et.amount as equity_owed_total
from owner o
left join current_owner_type cot on o.email = cot.email
left join owner_type ot on ot.owner_type = cot.owner_type
left join hour_balance h on o.email = h.email
left join hour_status s on
  coalesce(h.balance, 0) >= s.minimum_balance
  and coalesce(h.balance, 0) <= s.maximum_balance
left join owner_equity oe on o.email = oe.email
left join equity_type et on et.equity_type = oe.equity_type;
