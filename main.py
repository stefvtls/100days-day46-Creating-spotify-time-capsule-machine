import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import pprint

load_dotenv()
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
REDIRECT_URI = "http://example.com/"
id = os.getenv("ID")



historical_moment= input("Type in in the format YYYY-MM-DD the date that you would like to go back in time")
url = f"https://www.billboard.com/charts/hot-100/{historical_moment}/"
response = requests.get(url)
response.raise_for_status()
print(response.status_code)
bullion = response.text
soup = BeautifulSoup(bullion, "html.parser")

top100tags_titles = soup.find_all(name="h3", id='title-of-a-story', class_="a-no-trucate")
top100_titles = [title.getText().strip() for title in top100tags_titles]
print(top100_titles)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))
# user = sp.current_user()
# user_id = sp.current_user()["id"]

song_uris = []
year = historical_moment.split("-")[0]
for song in top100_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=id, name=f"{historical_moment} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
