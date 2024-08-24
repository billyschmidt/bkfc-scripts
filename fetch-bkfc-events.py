import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colorama
init()

# Fetch the HTML content from the BKFC events page
url = 'https://www.bkfc.com/events'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all event containers with the specific class
events = soup.find_all('div', class_='col-12 col-lg-4 mb-3')

# List to store event details
event_details = []

for event in events:
    # Extract event title
    title_tag = event.find('strong')
    title = title_tag.get_text(strip=True) if title_tag else 'No title'

    # Extract event date
    date_tag = event.find('small')
    date = date_tag.find('strong').get_text(strip=True) if date_tag and date_tag.find('strong') else 'No date'

    # Extract event location
    location_tag = date_tag.find('span', class_='text-muted') if date_tag else None
    location = location_tag.get_text(strip=True) if location_tag else 'No location'

    # Ensure that we only add events with valid titles
    if title != 'No title' and date != 'No date' and location != 'No location':
        event_details.append({
            'title': title,
            'date': date,
            'location': location
        })

# Print the event details with colors and spacing
print("\n")
for event in event_details:
    print(f"{Style.BRIGHT}{'-' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Title: {Fore.RESET}{event['title']}")
    print(f"{Fore.GREEN}Date: {Fore.RESET}{event['date']}")
    print(f"{Fore.MAGENTA}Location: {Fore.RESET}{event['location']}")
    print(f"{Style.BRIGHT}{'-' * 60}{Style.RESET_ALL}\n")
print("\n")
