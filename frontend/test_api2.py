from adzuna_client import adzuna

print("Testing Adzuna API...")
print("Searching for 'software engineer' jobs...")

jobs = adzuna.search_jobs('software engineer', '', 5)

print(f"Found {len(jobs)} jobs")

if jobs:
    print("\nFirst job found:")
    print(f"  Title: {jobs[0]['title']}")
    print(f"  Company: {jobs[0]['company']}")
    print(f"  Location: {jobs[0]['location']}")
else:
    print("\nNo jobs found. Trying different search...")
    
    # Try different search terms
    terms = ['python', 'developer', 'engineer', 'data']
    for term in terms:
        jobs2 = adzuna.search_jobs(term, '', 3)
        print(f"  '{term}': {len(jobs2)} jobs")