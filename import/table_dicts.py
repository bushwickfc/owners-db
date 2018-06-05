# The following three dicts are specific to the tables that data will be inserted into.
# Data from the list of owner data_dicts (as master_data) will be used to populate these dicts in insert.py.
owner_dict = {
    'old_member_id': None,
    'pos_id': None,
    'seven_shifts_id': None,
    'email': None,
    'first_name': None,
    'last_name': None,
    'join_date': None,
    'phone': None,
    'address': None,
    'city': None,
    'state': None,
    'zipcode': None,
    'payment_plan_delinquent': None
}
hour_log_dict = {
    'email': None,
    'amount': None,
    'hour_reason': None,
    'hour_date': None
} 
owner_owner_type_dict = {
    'email': None,
    'start_date': None,
    'owner_type': None
}