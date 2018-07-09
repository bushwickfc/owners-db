insert into owner_type(owner_type, display_name, pos_display, work_requirement,
                       work_surrogate, shopping_surrogate, owner_price) VALUES
('standard', 'Standard', '', 3, 0, 0, true),
('senior', 'Senior', ' // S', 2, 1, 1, true),
('parental', 'Parent/Guardian', ' // PG', 2, 1, 1, true),
('disability','Disabled/Injured', ' // DI', 0, 0, 1, true),
('pregnancy', 'Pregnancy', 'P', 0, 0, 1, true),
('family_leave', 'Family Leave', ' // FL', 0, 0, 1, true),
('hold', 'Hold', ' // H', 0, 0, 0, false),
('inactive', 'Inactive', ' // I', 0, 0, 0, false);

insert into hour_reason(hour_reason, display_name, description)  VALUES
('shift', 'Store Shift', 'In store shift'),
('other', 'Other',
 'If this is being used a lot, a new category should probably be created'),
('technology', 'Technology Committee', ''),
('ownership', 'Ownership Committee', ''),
('sourcing', 'Sourcing Committee', ''),
('facilities', 'Facilities Committee', ''),
('finance', 'Finance Committee', ''),
('governance', 'Governance Committee', ''),
('communications', 'Communications Committee', ''),
('environmental', 'Environmental Committee', ''),
('outreach', 'Outreach Committee', ''),
('board', 'Board', ''),
('balance_carryover', 'Balance Carryover',
 'Balance carried over from previous database'),
('penalty', 'Penalty', 'Missed shift penalty'),
('monthly_requirement','Monthly Requirement','Monthly work requirement'),
('meeting', 'Monthly coop meeting', 'Monthly coop wide committees meeeting');

insert into hour_status(status, display_name, pos_display, owner_price,
                        minimum_balance, maximum_balance) VALUES
('good_standing', 'Good Standing', 'Active', true, 0, 2147483647),
('hours_alert', 'Hours Alert', 'Hours Alert', true, -7, -1),
('hours_suspended', 'Hours Suspended', 'Hours Susp.', false, -2147483648,
-8);

insert into equity_round(equity_round, display_name, description) VALUES
('2018_initial', 'Initial 2018 equity round',
'The first round of equity after the transition to the equity model in 2018');

insert into equity_type(equity_round, equity_type, display_name,
                        description, amount, payment_plan_amount) VALUES
('2018_initial', 'full', 'Full Price', 'Full price equity share', 150.00,
 25.00),
('2018_initial', 'legacy', 'Legacy', 'Discounted equity share', 100.00,
 25.00),
('2018_initial', 'reduced', 'Reduced', 'Reduced equity share', 15.00,
 5.00);
