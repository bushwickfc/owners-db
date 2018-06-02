insert into owner_type(owner_type, display_name, work_requirement,
                       work_surrogate, shopping_surrogate, owner_price) VALUES
('standard', 'Standard', 3, 0, 0, true),
('senior', 'Senior', 2, 1, 1, true),
('parental', 'Parent/Guardian', 2, 1, 1, true),
('disability','Disabled/Injured', 0, 0, 1, true),
('pregnancy', 'Pregnancy', 0, 0, 1, true),
('family_leave', 'Family Leave', 0, 0, 1, true),
('hold', 'Hold', 0, 0, 0, false),
('inactive', 'Inactive', 0, 0, 0, false);

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
('board', 'Board', ''),
('balance_carryover', 'Balance Carryover',
 'Balance carried over from previous database'),
('penalty', 'Penalty', 'Missed shift penalty'),
('monthly_requirement','Monthly Requirement','Monthly work requirement');

insert into hour_status(status, display_name, pos_display, owner_price,
                        minimum_balance, maximum_balance) VALUES
('good_standing', 'Good Standing', ' // Active', true, 0, 2147483647),
('hours_alert', 'Hours Alert', ' // Hours Alert', true, -7, -1),
('hours_suspended', 'Hours Suspended', ' // Hours Susp.', false, -2147483648,
-8)
