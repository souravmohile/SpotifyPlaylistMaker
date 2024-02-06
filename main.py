import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# TODO: Setting Environment Variables
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

# TODO: Make Good Soup 👌🏻
date = input("What year would you wanna travel to? (Enter the date as YYYY-MM-DD): ")
URL = ("https://www.billboard.com/charts/hot-100/" + date)

response = requests.get(URL)
data = response.text

soup = BeautifulSoup(data, "html.parser")
title = soup.find_all(name="h3",
                      class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
                      id="title-of-a-story")

# TODO: Add All Names of Songs to a List
names_list = [movie.getText() for movie in title]
movies = [name.replace("\n", "") for name in names_list]

first = soup.find(name="a", class_="c-title__link lrv-a-unstyle-link")
movies.insert(0, first.getText().replace("\n", ""))

# TODO: Authenticate Spot
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# TODO: Search Song on Spotify
song_uris = []
year = date.split("-")[0]
for song in movies:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# TODO: Create a Playlist and Add All the Songs to It
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date} Billboard Top 100",
                                   public=False,
                                   description='Playlist created with python'
                                   )

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)




