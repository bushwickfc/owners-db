insert into owner(email, first_name, last_name, display_name, join_date) values
('owner1@example.com', 'owner', 'one', 'owner one', '2018-04-20');

insert into owner_owner_type (email, owner_type, start_date) values
('owner1@example.com', 'standard', '2018-04-20');

insert into household (household, email) values
('household1', 'owner1@example.com');

insert into hour_log (email, amount, hour_reason, hour_date) values
('owner1@example.com', 4, 'technology', '2018-04-20'),
('owner1@example.com', -4, 'monthly_requirement', '2018-04-01'),
('owner1@example.com', -4, 'monthly_requirement', '2018-04-02');
