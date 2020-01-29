import sys
import json

request = {
    'method': 'GET',
    'url': f'http://localhost:80/'
}
sys.stdout.write(f'{json.dumps(request)}\n')
