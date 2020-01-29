import sys
import json

request = {
    'method': 'GET',
    'url': f'http://localhost:8000/test_no_db'
}
sys.stdout.write(f'{json.dumps(request)}\n')
