alter table hour_log drop constraint hour_log_pkey;

alter table hour_log add column id serial primary key;

create index email_hour_log_hour_reason on hour_log (email, hour_reason);
