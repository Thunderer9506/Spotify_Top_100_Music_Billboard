from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID="Your Client Id"

CLIENT_SECRET = "Your Client Secret"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL =f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)

webpage=response.text

soup = BeautifulSoup(webpage,"html.parser")

heading = soup.find_all('div', class_='o-chart-results-list-row-container')

song_names= [head.find('h3').text.strip() for head in heading]

scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

add_songs = sp.playlist_add_items(playlist_id='Your playlist ID',items=song_uris)