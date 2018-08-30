alter table owner_owner_type drop constraint owner_owner_type_pkey;

alter table owner_owner_type add column id serial primary key;

create unique index email_start_date_owner_type on owner_owner_type (email, start_date, owner_type);
