insert into owner_type(owner_type, display_name, work_requirement,
                       work_surrogate, shopping_surrogate, owner_price) VALUES
('standard', 'Standard', 3, 0, 0, 1),
('senior', 'Senior', 2, 1, 1, 1),
('parental', 'Parent/Guardian', 2, 1, 1, 1),
('disability','Disabled/Injured', 0, 0, 1, 1),
('pregnancy', 'Pregnancy', 0, 0, 1, 1),
('family_leave', 'Family Leave', 0, 0, 1, 1),
('hold', 'Hold', 0, 0, 0, 0)

insert into hour_reason(hour_reason, display_name, description)  VALUES
('shift', 'Store Shift', 'In store shift'),
('other', 'Other',
 'If this is being used a lot, a new category should probably be created'),
('technology', 'Technology Committee', ''),
('membership', 'Membership Committee', ''),
('sourcing', 'Sourcing Committee', ''),
('facilities', 'Facilities Committee', ''),
('finance', 'Finance Committee', ''),
('governance', 'Governance Committee', ''),
('communications', 'Communications Committee', ''),
('environmental', 'Environmental Committee', ''),
('outreach', 'Outreach Committee', ''),
('board', 'Board', '')

insert into equity_round(equity_round, display_name, description) VALUES
('2018_initial', 'Initial 2018 equity round',
'The first round of equity after the transition to the equity model in 2018')

insert into equity_type(equity_round, equity_type, display_name,
                        description, amount) VALUES
('2018_initial', 'full', 'Full Price', 'Full price equity share', 150.00),
('2018_initial', 'legacy', 'Legacy', 'Discounted equity share', 100.00),
('2018_initial', 'reduced', 'Reduced', 'Reduced equity share', 15.00)
