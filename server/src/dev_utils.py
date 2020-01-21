import requests
import json
import random
import datetime
from constants import STATUS
from russian_names import RussianNames
from functools import reduce


def get_city_sample_space(precision=5000, src_path='data/russian_cities.json'):
    sample_space = []
    with open(src_path) as cities_file:
        cities = json.load(cities_file)
        for city in cities:
            city_name = city['name_en'].replace("'", "").replace(" ", "")
            sample_space += [city_name] * (city['population'] // precision)

    return sample_space


def get_names_sample_space(size=1000, batch_size=1000):
    batch_count = max(1, size // batch_size)
    generator = RussianNames(count=batch_size, patronymic=False, transliterate=True)
    raw_samples = reduce(lambda a, b: a + b, (generator.get_batch() for _ in range(batch_count)), ())
    sample_space = [raw.replace("'", "").split() for raw in raw_samples]

    return sample_space


def get_age_sample_space():
    lo = 14
    distribution = [(17, 15), (24, 50), (34, 39), (44, 18), (54, 8), (64, 3), (79, 1)]

    sample_space = []
    for hi, p in distribution:
        for age in range(lo, hi + 1):
            sample_space += [age] * p
        lo = hi + 1

    return sample_space


def sample_birth_date(age_sample_space, today_date):
    age = random.choice(age_sample_space)
    days = int(365.25 * (age + random.random()))
    return today_date - datetime.timedelta(days=days)


def get_user_list(user_ids, url='http://localhost:80'):
    r = requests.get(f'{url}/user_list_full', json={'user_ids': user_ids})
    return r.json() if r.status_code == STATUS.SUCCESS else None


def get_max_user_id(url='http://localhost:80'):
    r = requests.get(f'{url}/max_user_id')
    return r.json()['user_id'] if r.status_code == STATUS.SUCCESS else None
