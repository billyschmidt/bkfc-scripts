import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Get email credentials from environment variables
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("SECRET")

def send_email(event_details):
    from_email = email_address
    reply_to_email = email_address
    to_email = email_address

    subject = "BKFC Event Notifications"
    body_template = """
    <html>
    <head>
        <style>
            .container {{
                font-family: Arial, sans-serif;
                color: #333;
                margin: 20px;
            }}
            h2 {{
                color: #D32F2F;
                text-align: center;
            }}
            .event {{
                border: 1px solid #ccc;
                padding: 10px;
                margin-bottom: 15px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .title {{
                font-weight: bold;
                color: #007BFF;
                font-size: 18px;
            }}
            .date, .location {{
                color: #555;
                font-size: 14px;
            }}
            .separator {{
                border-top: 1px solid #ddd;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Upcoming BKFC Events</h2>
            {event_html}
        </div>
    </body>
    </html>
    """

    # Generate the HTML content for each event
    event_html = ""
    for event in event_details:
        event_html += f"""
        <div class="event">
            <div class="title">{event['title']}</div>
            <div class="date"><strong>Date:</strong> {event['date']}</div>
            <div class="location"><strong>Location:</strong> {event['location']}</div>
        </div>
        <div class="separator"></div>
        """

    # Insert the event HTML into the body
    body = body_template.format(event_html=event_html)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Reply-To'] = reply_to_email  # Set the Reply-To header
    msg.attach(MIMEText(body, 'html'))

    try:
        # Use SMTP_SSL instead of SMTP for port 465
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, email_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

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

# Send email with event details
send_email(event_details)
