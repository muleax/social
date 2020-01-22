import random
import sys
import base64
import json
import datetime
sys.path.append("../src")
from dev_utils import *


DATA_SRC_URL = 'http://localhost:8000'
TEST_URL = 'http://localhost:8000'

# 0 - exclusively read
# 1 - exclusively write
READ_WRITE_RATIO = 0

class READ_PROBABILITY:
    LAST_NAME = 0.5
    FIRST_NAME = 0.5
    CITY = 0.5
    AGE = 0.5
    MISS = 0.3


cities = get_city_sample_space(src_path='../src/data/russian_cities.json')
names = get_names_sample_space(size=100000)
ages = get_age_sample_space()

max_user_id = get_max_user_id(DATA_SRC_URL)
users = get_user_list(list(random.randint(1, max_user_id) for _ in range(50000)), DATA_SRC_URL)

today_date = datetime.date.today()

for _ in range(80000):
    user_data = random.choice(users)
    name = random.choice(names)

    if random.random() > READ_WRITE_RATIO:  # Read
        if random.random() < READ_PROBABILITY.MISS:
            name_postfix, age_shift = 'missread', 1000
        else:
            name_postfix, age_shift = '', 0

        params = []
        while True:
            if random.random() < READ_PROBABILITY.LAST_NAME:
                params.append(f'last_name={name[1]}{name_postfix}')

            if random.random() < READ_PROBABILITY.FIRST_NAME:
                params.append(f'first_name={name[0]}{name_postfix}')

            if random.random() < READ_PROBABILITY.CITY:
                params.append(f'city={random.choice(cities)}{name_postfix}')

            if random.random() < READ_PROBABILITY.AGE:
                age1, age2 = random.choice(ages), random.choice(ages)
                params.append(f'age_from={min(age1, age2) + age_shift}')
                params.append(f'age_to={max(age1, age2) + age_shift}')

            if params:
                params += [f'user_id={user_data["user_id"]}', f'auth_token={user_data["auth_token"]}', 'offset=0', 'limit=10']
                params_uri = '&'.join(params)
                request = {
                    'method': 'GET',
                    'url': f'{TEST_URL}/find_users?{params_uri}'
                }
                break

    else:  # Write
        body = {
            'user_id': user_data['user_id'],
            'auth_token': user_data['auth_token'],
            'city': random.choice(cities),
            'first_name': name[0],
            'last_name': name[1],
            'birth_date': sample_birth_date(ages, today_date).isoformat(),
            'udata': '{}'
        }
        request = {
            'method': 'POST',
            'url': f'{TEST_URL}/update_user',
            'body': base64.b64encode(json.dumps(body).encode('utf-8')).decode()
        }

    sys.stdout.write(f'{json.dumps(request)}\n')
