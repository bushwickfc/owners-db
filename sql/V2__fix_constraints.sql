alter table owner_owner_type drop constraint owner_owner_type_email_fkey;
alter table owner_owner_type add foreign key (email)
references owner(email) on update cascade on delete cascade;

alter table hour_log drop constraint hour_log_email_fkey;
alter table hour_log add foreign key (email) references
owner(email) on update cascade on delete cascade;

alter table owner_equity_type drop constraint owner_equity_type_email_fkey;
alter table owner_equity_type add foreign key (email) references
owner(email) on update cascade on delete cascade;

alter table equity_log drop constraint equity_log_email_fkey;
alter table equity_log add foreign key (email) references
owner(email) on update cascade on delete cascade;
