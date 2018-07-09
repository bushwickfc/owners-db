from datetime import datetime

import requests

import credentials
import util

SHIFTS_URL = "https://api.7shifts.com/v1/shifts"
TIME_FMT = "%Y-%m-%d %H:%M:%S"

MANAGERS = ["fran@bushwickfoodcoop.org",
            "laurel@bushwickfoodcoop.org",
            ""]

def fetch_shifts(start_date, end_date):
    returned = None
    offset = 0
    data = []
    while (returned is None) or (returned > 0):
        params = {'start[gte]':start_date,
                  'start[lte]':end_date,
                  'deep':'1',
                  'open':'0',
                  'deleted':'0',
                  'offset':offset,
                  'limit':'500'}
        r = requests.get(SHIFTS_URL,params=params,
                         auth=(credentials.seven_shifts_api_key, ''))
        resp = r.json()
        if resp['status'] != 'success':
            # error out if not successful
            raise ValueError
        else:
            offset = offset + resp['total']
            returned = len(resp['data'])
            data = data + resp['data']
    return data

def transform(resp_obj):
    user = resp_obj['user']
    shift = resp_obj['shift']
    start = datetime.strptime(shift['start'], TIME_FMT)
    end = datetime.strptime(shift['end'], TIME_FMT)
    hours = (end - start).total_seconds() / 3600
    return {'email': util.normalize_email(user['email']),
            'seven_shifts_id': user['id'],
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'shift_start': start,
            'shift_end': end,
            'hours': hours}

def insert(conn, user_shifts):
    owners = util.existing(conn, 'owner')
    query = """insert into hour_log(email, amount, hour_date, hour_reason) \
             values (%(email)s, %(hours)s, %(shift_start)s, 'shift')"""
    user_shifts_ins = [s for s in user_shifts if
                       s['email'] in owners]
    user_shifts_not_ins = [s for s in user_shifts if
                           s['email'] not in owners]
    with conn.cursor() as cursor:
        cursor.executemany(query, user_shifts_ins)
    return user_shifts_not_ins
