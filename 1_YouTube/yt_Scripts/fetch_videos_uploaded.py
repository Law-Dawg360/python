from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Your API key
API_KEY = os.environ['API_KEY']

# Function to read channel IDs from file
def read_channel_ids(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Function to fetch latest videos uploaded on the current day
def fetch_latest_videos():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get the current date in ISO 8601 format
    current_date = datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')

    # Read channel IDs from file
    CHANNEL_IDS = read_channel_ids('channel_ids.txt')

    for channel_id in CHANNEL_IDS:
        try:
            # Get the uploads playlist ID for the channel
            channel_info = youtube.channels().list(part='contentDetails,snippet', id=channel_id).execute()
            uploads_playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Get the latest videos from the uploads playlist
            playlist_items = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=10  # Adjust this number as needed
            ).execute()

            # Process each video in the playlist
            for item in playlist_items['items']:
                video_published_at = item['snippet']['publishedAt']
                
                # Check if the video was published today
                if video_published_at >= current_date:
                    video_id = item['snippet']['resourceId']['videoId']
                    video_title = item['snippet']['title']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    video_thumbnail = item['snippet']['thumbnails']['default']['url']
                    video_duration = get_video_duration(youtube, video_id)

                    # Print or store the information as needed
                    print("Uploader:", channel_info['items'][0]['snippet']['title'])
                    print("Video URL:", video_url)
                    print("Title:", video_title)
                    print("Thumbnail:", video_thumbnail)
                    print("Published At:", video_published_at)
                    print("Duration:", video_duration)
                    print("\n")
        except KeyError:
            print(f"Unable to fetch information for channel with ID {channel_id}")

# Function to get video duration
def get_video_duration(youtube, video_id):
    video_info = youtube.videos().list(
        part='contentDetails',
        id=video_id
    ).execute()

    duration = video_info['items'][0]['contentDetails']['duration']
    return parse_duration(duration)

# Function to parse duration in ISO 8601 format to seconds
def parse_duration(duration):
    duration = duration[2:]  # Remove the leading 'PT'
    seconds = 0

    # Parse days, hours, minutes, seconds
    if 'D' in duration:
        days, duration = duration.split('D')
        seconds += int(days) * 86400
    if 'H' in duration:
        hours, duration = duration.split('H')
        seconds += int(hours) * 3600
    if 'M' in duration:
        minutes, duration = duration.split('M')
        seconds += int(minutes) * 60
    if 'S' in duration:
        seconds += int(duration.split('S')[0])

    return seconds

# Call the function to fetch latest videos uploaded on the current day
fetch_latest_videos()
