import sqlite3
import datetime
import openai

# Initialize GPT-4 model
OPENAI_API_KEY = 'YOUR API KEY'
openai.api_key = OPENAI_API_KEY

# Connect to the Chrome history database
conn = sqlite3.connect('C:/Users/[USER]/AppData/Local/Google/Chrome/User Data/Default/History')

# Define the start and end times for the query (yesterday's date)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
start_time = int((datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0) - datetime.datetime(1601, 1, 1)).total_seconds() * 1000000)
end_time = int((datetime.datetime(today.year, today.month, today.day, 0, 0, 0) - datetime.datetime(1601, 1, 1)).total_seconds() * 1000000)

# Execute the query to get the URLs and titles of the websites visited yesterday
query = "SELECT url, title, last_visit_time FROM urls WHERE last_visit_time BETWEEN ? AND ?"
result = conn.execute(query, (start_time, end_time))

# Extract the domain names from the URLs and count their occurrences
domain_counts = {}
for row in result:
    url = row[0]
    domain = url.split('/')[2]
    if domain in domain_counts:
        domain_counts[domain] += 1
    else:
        domain_counts[domain] = 1

# Generate the list of visited URLs in a format that GPT-4 can understand
visited_urls = "\n".join(f"- {domain}: {count} visits" for domain, count in domain_counts.items())

# Ask GPT-4 to interpret your browsing history
messages = [{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Here is a list of URLs and visit counts:\n\n{visited_urls}\n\nBased on this list, what have I been working on yesterday?"}]

#response = openai.ChatCompletion.create(
#    model="gpt-4",
#    messages=messages,
#    max_tokens=50,
#    n=1,
#    stop=None,
#    temperature=0.5,
response = openai.ChatCompletion.create(
    model="text-davinci-002",
    messages=messages,
    max_tokens=50,
    n=1,
    stop=None,
    temperature=0.5,
)

print(response.choices[0].text.strip())
