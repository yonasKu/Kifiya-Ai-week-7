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

        message_counter = 1  # Counter to generate unique message IDs if missing

        # Iterate over each message in the HTML and extract relevant data
        for message in messages:
            # Get the message ID, handle cases where ID is missing
            message_id = message.get('id')
            if not message_id or message_id == "0":  # If no ID or ID is '0', generate a unique ID
                message_id = f"msg_{message_counter}"
                message_counter += 1

            # Extract 'date' information from service or default messages
            date_div = message.find('div', class_='pull_right date details') or message.find('div', class_='body details')
            date = date_div.text.strip() if date_div else 'Unknown Date'

            # Extract 'from_name' (sender)
            from_name_div = message.find('div', class_='from_name')
            from_name = from_name_div.text.strip() if from_name_div else 'Unknown Sender'

            # Extract message text
            text_div = message.find('div', class_='text')
            message_text = text_div.text.strip() if text_div else ''

            # Handle any potential media links (if any exist, modify as needed)
            media_path = ''  # Currently empty, modify logic if necessary

            # Write each message data to CSV
            writer.writerow([from_name, '', message_id, message_text, date, media_path])

    print(f"Scraping complete! Data saved to {csv_file_path}")

# # Example usage
# html_file_path = 'path_to_your_html_file.html'
# scrape_html_to_csv(html_file_path)
