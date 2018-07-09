create table owner_type (
  owner_type varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  pos_display varchar(10) NOT NULL,
  description varchar(255),
  work_requirement int NOT NULL,
  work_surrogate int NOT NULL,
  shopping_surrogate int NOT NULL,
  owner_price boolean NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_type)
);

create table owner (
  old_member_id int,
  pos_id varchar(255),
  seven_shifts_id varchar(255),
  email varchar(254) NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL,
  join_date date NOT NULL,
  phone varchar(10),
  address text,
  city text,
  state text,
  zipcode varchar(10),
  payment_plan_delinquent boolean,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (email)
);

create table owner_owner_type (
  email varchar(255) NOT NULL,
  owner_type varchar(20) NOT NULL,
  start_date date NOT NULL,
  end_date date,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(email, start_date),
  FOREIGN KEY (owner_type)
  REFERENCES owner_type(owner_type)
  ON UPDATE CASCADE,
  FOREIGN KEY (email)
  REFERENCES owner(email)
  ON UPDATE CASCADE
);

create table household (
  household varchar(255),
  email varchar(254),
  PRIMARY KEY (household, email),
  FOREIGN KEY (email)
  REFERENCES owner(email)
  ON UPDATE CASCADE
);

create table hour_reason (
  hour_reason varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(hour_reason)
);

create table hour_log (
  email varchar(254) NOT NULL,
  amount int NOT NULL,
  hour_reason varchar(20) NOT NULL,
  hour_date timestamp NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(email, hour_reason, hour_date),
  FOREIGN KEY(hour_reason)
  REFERENCES hour_reason(hour_reason)
  ON UPDATE CASCADE,
  FOREIGN KEY(email)
  REFERENCES owner(email)
  ON UPDATE CASCADE
);

create table equity_round (
  equity_round varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(equity_round)
);

create table equity_type (
  equity_round varchar(20) NOT NULL,
  equity_type varchar(20) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_plan_amount DECIMAL(10,2) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(equity_type),
  FOREIGN KEY(equity_round)
  REFERENCES equity_round(equity_round)
  ON UPDATE CASCADE
);

create table owner_equity_type (
  email varchar(254) NOT NULL,
  equity_type varchar(20) NOT NULL,
  start_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(email, equity_type),
  FOREIGN KEY (email)
  REFERENCES owner(email)
  ON UPDATE CASCADE,
  FOREIGN KEY(equity_type)
  REFERENCES equity_type(equity_type)
  ON UPDATE CASCADE
);

create table equity_log (
  email varchar(254) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  transaction_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(email, transaction_date),
  FOREIGN KEY(email)
  REFERENCES owner(email)
  ON UPDATE CASCADE
);

create table hour_status (
  status varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  pos_display varchar(255) NOT NULL,
  minimum_balance int NOT NULL,
  maximum_balance int NOT NULL,
  owner_price boolean NOT NULL,
  PRIMARY KEY(status)
);

create view hour_balance as
select
  email,
  sum(amount) as balance
from hour_log
group by email;

create view current_owner_type as
select
  distinct
  email,
  max(owner_type) over (partition by email order by start_date desc)
    as owner_type
from owner_owner_type;

create view owner_equity as
select *,
  paid >= due as owner_price,
  case when paid < due then concat(' // ', paid - due)
       else ''
  end  as pos_display
  from
  (select
    oet.email,
    sum(el.amount) as paid,
    /* owe an installment every month until we reach full amount */
    least(
      (((DATE_PART('year', CURRENT_DATE) -
         DATE_PART('year', oet.start_date)) * 12
         + (DATE_PART('month', CURRENT_DATE) -
         DATE_PART('month', oet.start_date)))
           * et.payment_plan_amount),
      et.amount) as due
    from (
      /* legacy payment plans get an extra month to repay since they don't
       have to pay a fee */
      select email,
      equity_type,
      start_date - interval '1 month' as start_date
      from owner_equity_type
      where equity_type='legacy'
      union
      select email,
      equity_type,
      start_date
      from owner_equity_type
      where equity_type != 'legacy') oet
    join equity_type et on oet.equity_type = et.equity_type
    join equity_log el on oet.email = el.email
    group by oet.email, oet.start_date, et.payment_plan_amount, et.amount) as s;

create view owner_view as
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
  (NOT (oe.owner_price AND s.owner_price AND ot.owner_price))::int + 1,
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
  oe.owner_price as equity_current,
  s.owner_price as hours_current,
  (oe.owner_price AND s.owner_price AND ot.owner_price)
    as owner_price
from owner o
join current_owner_type cot on o.email = cot.email
join owner_type ot on ot.owner_type = cot.owner_type
left join hour_balance h on o.email = h.email
join hour_status s on
  coalesce(h.balance, 0) >= s.minimum_balance
  and coalesce(h.balance, 0) <= s.maximum_balance
join owner_equity oe on o.email = oe.email;
