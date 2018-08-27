create or replace view owner_equity as
select
  email,
  paid,
  due,
  paid >= due as owner_price,
  case when paid < due then concat(' // ', paid - due)
       else ''
  end as pos_display,
  plan_join_date,
  first_due_date
  from
  (select
    oet.email,
    coalesce(sum(el.amount), 0) as paid,
    /* owe an installment every month until we reach full amount */
    least(
      (((DATE_PART('year', CURRENT_DATE) -
         DATE_PART('year', oet.effective_start_date)) * 12
         + (DATE_PART('month', CURRENT_DATE) -
         DATE_PART('month', oet.effective_start_date)))
           * et.payment_plan_amount),
      et.amount) as due,
      oet.start_date as plan_join_date,
      oet.effective_start_date as first_due_date
    from (
      /* non-legacy payment plans get an extra month to repay since they
         have to pay a fee the first month rather than a payment */
      select email,
      equity_type,
      start_date + interval '1 month' as effective_start_date,
      start_date
      from owner_equity_type
      where equity_type != 'legacy'
      union
      select email,
      equity_type,
      start_date,
      start_date as effective_start_date
      from owner_equity_type
      where equity_type = 'legacy') oet
    join equity_type et on oet.equity_type = et.equity_type
    left join equity_log el on oet.email = el.email
    group by oet.email, oet.effective_start_date, oet.start_date,
    et.payment_plan_amount, et.amount) as s;

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
  oe.plan_join_date
from owner o
left join current_owner_type cot on o.email = cot.email
left join owner_type ot on ot.owner_type = cot.owner_type
left join hour_balance h on o.email = h.email
left join hour_status s on
  coalesce(h.balance, 0) >= s.minimum_balance
  and coalesce(h.balance, 0) <= s.maximum_balance
left join owner_equity oe on o.email = oe.email;
