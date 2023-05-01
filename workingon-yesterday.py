import sqlite3
import datetime

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
    visit_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=row[2])
    print("- " + domain + ":\n  - Title: " + row[1] + "\n  - Last Visit Time: " + visit_time.strftime('%Y-%m-%d %H:%M:%S'))

# Print the results
if not domain_counts:
    print("No browsing history found for", yesterday.strftime("%Y-%m-%d"))
else:
    print("Summary of your browsing history for " + str(yesterday) + ":")
    for domain, count in domain_counts.items():
        print("- " + domain + ": " + str(count) + " visits")
