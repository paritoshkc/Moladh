import json
from src import FinalVariables
from src import database
import requests


class GenreDetails:
    genres = []

    def __init__(self, genres):
        self.genres = genres


database = database.Database()
conn = database.createConnection()
database.createTables(conn)


def fetch_genres():
    api_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + FinalVariables.getAPIKey() + '&language=en-US'
    headers = {}
    response = requests.get(api_url, headers=headers)
    print(response)
    if response.status_code == 200:
        data = json.loads(response.content)
        GenreDetails(data)
        genres = data['genres']
        for i in genres:
            database.input_genre(conn, i['id'], i['name'])
    else:
        print('Error')
        return 0


fetch_genres()