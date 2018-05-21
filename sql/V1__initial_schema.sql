START TRANSACTION;
create table owner_type (
  owner_type varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  work_requirement int NOT NULL,
  work_surrogate int NOT NULL,
  shopping_surrogate int NOT NULL,
  owner_price bit(1) NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_type)
);

create table owner (
  old_member_id int,
  pos_id varchar(255),
  seven_shifts_id varchar(255),
  email varchar(254) NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL,
  display_name text,
  join_date date NOT NULL,
  phone varchar(10),
  address text,
  city text,
  state text,
  zipcode varchar(9),
  payment_plan_delinquent bit(1),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (email)
);

create table owner_owner_type (
  email varchar(255) NOT NULL,
  owner_type varchar(20) NOT NULL,
  start_date date NOT NULL,
  end_date date,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(hour_reason)
);

create table hour_log (
  email varchar(254) NOT NULL,
  amount int NOT NULL,
  hour_reason varchar(20) NOT NULL,
  hour_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(email, hour_reason, hour_date),
  FOREIGN KEY(hour_reason)
  REFERENCES hour_reason(hour_reason)
  ON UPDATE CASCADE,
  FOREIGN KEY(email)
  REFERENCES owner(email)
  ON UPDATE CASCADE
);

create table equity_log (
  email varchar(254) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  transaction_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
  owner_price bit(1) NOT NULL,
  PRIMARY KEY(status)
);

create sql security invoker view hour_balance as
select
  email,
  sum(amount) as balance
from hour_log
group by email;

create sql security invoker view current_owner_type as
select
  distinct
  email,
  max(owner_type) over (partition by email order by start_date desc)
    as owner_type
from owner_owner_type;

create sql security invoker view owner_view as
select
  o.pos_id,
  ot.owner_type,
  ot.display_name as owner_type_name,
  s.status,
  o.email,
  o.first_name,
  o.last_name,
  concat(o.display_name, s.pos_display, CONVERT(pp.pos_display USING latin1)) as pos_display,
  coalesce(h.balance, 0) as hour_balance,
  (coalesce(pp.owner_price, 0) & s.owner_price & ot.owner_price)
    as owner_price
from owner o
join current_owner_type cot on o.email = cot.email
join owner_type ot on ot.owner_type = cot.owner_type
left join hour_balance h on o.email = h.email
join hour_status s on
  coalesce(h.balance, 0) >= s.minimum_balance
  and coalesce(h.balance, 0) <= s.maximum_balance
left join (select
    ' // Equity Susp.' as pos_display,
    0 as owner_price) pp
  on o.payment_plan_delinquent = 1;

COMMIT;
