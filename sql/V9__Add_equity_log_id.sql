alter table equity_log drop constraint equity_log_pkey;

alter table equity_log add column id serial primary key;

create index equity_log_email_transaction_date
  on equity_log (email, transaction_date);
