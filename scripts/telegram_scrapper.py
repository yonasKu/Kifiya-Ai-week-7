from telethon import TelegramClient, types
import csv
import os
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('.env')
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('phone')

# Set up logging to display in the notebook or console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize file names
def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        logging.info(f"Scraping started for {channel_title} ({channel_username})")

        async for message in client.iter_messages(entity, limit=4000):
            media_path = None

            if message.media:
                if hasattr(message.media, 'photo'):
                    # Handle photo media
                    filename = sanitize_filename(f"{channel_username}_{message.id}.jpg")
                    media_path = os.path.join(media_dir, filename)
                    await client.download_media(message.media, media_path)
                    logging.info(f"Downloaded photo: {media_path}")

                elif hasattr(message.media, 'document'):
                    # Handle document media
                    doc_attributes = message.media.document.attributes
                    if doc_attributes:
                        # Check for filename in the document attributes
                        for attr in doc_attributes:
                            if isinstance(attr, types.DocumentAttributeFilename):
                                filename = sanitize_filename(f"{channel_username}_{message.id}_{attr.file_name}")
                                media_path = os.path.join(media_dir, filename)
                                await client.download_media(message.media, media_path)
                                logging.info(f"Downloaded document: {media_path}")
                                break
                        else:
                            # If no filename found, use a default name
                            filename = sanitize_filename(f"{channel_username}_{message.id}.bin")
                            media_path = os.path.join(media_dir, filename)
                            await client.download_media(message.media, media_path)
                            logging.info(f"Downloaded file with no name: {media_path}")

                # You can add more media types like video, audio, etc. here as needed

            # Write the channel title along with other data to CSV
            writer.writerow([
                channel_title, channel_username, message.id, 
                message.message or '',  # Ensure message is not None
                message.date.isoformat(),  # Format the date
                media_path or ''  # Handle case where no media is present
            ])
        
        logging.info(f"Finished scraping {channel_title}")

    except Exception as e:
        logging.error(f"Error occurred while scraping {channel_username}: {str(e)}")

# Initialize the Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Modify the main function to use async with
async def main():
    async with client:
        await client.start()

        # Create a directory for media files (photos/documents)
        media_dir = 'media_files'
        os.makedirs(media_dir, exist_ok=True)

        # Open the CSV file and prepare the writer
        with open('data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # CSV headers including channel title
            writer.writerow(['Channel Title', 'Channel Username', 'Message ID', 'Message Text', 'Date', 'Media Path'])

            # List of channels to scrape (Ethiopian medical business channels)
            channels = [
                'https://t.me/DoctorsET',        # Ethiopian medical business channel
                'https://t.me/lobelia4cosmetics', # Cosmetics and pharmaceutical products
                'https://t.me/yetenaweg',         # Ethiopian medical services
                'https://t.me/EAHCI',             # Ethiopian Allied Health Council International
                'https://t.me/ChemedTelegramChannel', # Ethiopian Chemed channel
            ]

            # Iterate over channels and scrape data
            for channel in channels:
                logging.info(f"Starting to scrape data from {channel}")
                print(f"Scraping data from {channel}...")
                await scrape_channel(client, channel, writer, media_dir)
                print(f"Finished scraping data from {channel}")
                logging.info(f"Finished scraping data from {channel}")

# This part can remain if you are running this script normally in Python, but will not be needed in Jupyter
if __name__ == "__main__":
    import asyncio
    # Use asyncio.run() to handle async code if run from a script
    asyncio.run(main())
