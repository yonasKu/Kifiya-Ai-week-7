import csv
from bs4 import BeautifulSoup
import os

# Function to sanitize file names
def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()

# Function to convert HTML messages to CSV format
def scrape_html_to_csv(html_file_path):
    # Extract the base name of the HTML file and create a CSV file path
    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    csv_file_path = os.path.join(os.path.dirname(html_file_path), f"{base_name}.csv")
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    # Open the CSV file to write
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # CSV headers
        writer.writerow(['Channel Title', 'Channel Username', 'Message ID', 'Message Text', 'Date', 'Media Path'])

        # Extract messages from the HTML
        messages = soup.find_all('div', class_='message')

        # Iterate over each message in the HTML and extract relevant data
        for message in messages:
            message_id = message.get('id', '')
            date_div = message.find('div', class_='date')
            from_name_div = message.find('div', class_='from_name')
            text_div = message.find('div', class_='text')
            
            # Extract text from HTML elements, handle missing elements gracefully
            date = date_div.text.strip() if date_div else ''
            from_name = from_name_div.text.strip() if from_name_div else 'Unknown Sender'
            message_text = text_div.text.strip() if text_div else ''
            media_path = ''  # Placeholder for media path (modify if extracting media)

            # Write each message data to CSV
            writer.writerow([from_name, '', message_id, message_text, date, media_path])

    print(f"Scraping complete! Data saved to {csv_file_path}")
