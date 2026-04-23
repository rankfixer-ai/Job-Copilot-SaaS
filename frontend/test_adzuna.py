import requests

APP_ID = 'cba1c51a'
APP_KEY = '39f3605c39092b40573b341e883f06f6'

url = 'https://api.adzuna.com/v1/api/jobs/us/search/1'
params = {
    'app_id': APP_ID,
    'app_key': APP_KEY,
    'results_per_page': 10,
    'what': 'developer',
    'where': 'new york'
}

response = requests.get(url, params=params)
data = response.json()
results = data.get('results', [])

print(f'Total results found: {data.get(\"count\", 0)}')
print(f'Jobs returned: {len(results)}')

if results:
    for job in results[:3]:
        print(f'\n📌 {job.get(\"title\", \"N/A\")}')
        print(f'   Company: {job.get(\"company\", {}).get(\"display_name\", \"N/A\")}')
        print(f'   Location: {job.get(\"location\", {}).get(\"display_name\", \"N/A\")}')
"