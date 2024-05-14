from googleapiclient.discovery import build

# Your API key
API_KEY = os.environ['API_KEY']

# Function to read channel IDs from file
def read_channel_ids(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Function to get channel information
def get_channel_info():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Read channel IDs from file
    CHANNEL_IDS = read_channel_ids('channel_ids.txt')

    for channel_id in CHANNEL_IDS:
        try:
            # Get channel information
            channel_info = youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()

            # Extract channel name, profile picture, and subscriber count
            channel_name = channel_info['items'][0]['snippet']['title']
            profile_picture = channel_info['items'][0]['snippet']['thumbnails']['default']['url']
            subscriber_count = channel_info['items'][0]['statistics']['subscriberCount']

            # Print or store the information as needed
            print("Channel Name:", channel_name)
            print("Profile Picture:", profile_picture)
            print("Subscriber Count:", subscriber_count)
            print("\n")
        except Exception as e:
            print(f"Error fetching information for channel with ID {channel_id}: {str(e)}")

# Call the function to get channel information
get_channel_info()
