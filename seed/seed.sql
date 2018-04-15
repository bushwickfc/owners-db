insert into owner_type(owner_type, display_name, description) VALUES
('household', 'Household', 'Household membership'),
('individual', 'Individual', 'Individual membership, default terms')

insert into hour_reason(hour_reason, display_name, description)  VALUES
('shift', 'Store Shift', 'In store shift'),
('other', 'Other',
 'If this is being used a lot, a new category should probably be created'),
('technology', 'Technology Committee', ''),
('membership', 'Membership Committee', '')

insert into equity_round(equity_round, display_name, description) VALUES
('2018_initial', 'Initial 2018 equity round',
'The first round of equity after the transition to the equity model in 2018')

insert into equity_type(equity_round, equity_type, display_name,
                        description, amount) VALUES
('2018_initial', 'full', 'Full Price', 'Full price equity share', 150.00),
('2018_initial', 'legacy', 'Legacy', 'Discounted equity share', 100.00),
('2018_initial', 'reduced', 'Reduced', 'Reduced equity share', 15.00)
