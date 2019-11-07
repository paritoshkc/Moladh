import requests
import json
from src import database
from src import FinalVariables
import urllib.parse

database = database.Database()
conn = database.createConnection()


def user_watches_movie(user_id, movie_details, like):
    database.input_movie_watched(conn, user_id, movie_details['id'], like)
    update_user_preferences(user_id, movie_details)


def filter_users_movies():
    user_watched_movies = database.fetch_users_watched_movies(conn)
    watched_movies_id = []
    for i in user_watched_movies:
        watched_movies_id.append(i[0])

    no_of_movies = FinalVariables.get_number_of_movies_to_be_displayed()
    user_genre_preferences = database.fetch_users_preferences(conn)
    genre_weight = {}
    for i in user_genre_preferences:
        weight = (i[1] * no_of_movies) / 100
        genre_weight[str(i[0])] = round(weight)
    print(user_genre_preferences)
    print(genre_weight)
    filtered_results = []
    for i in user_genre_preferences:
        results = fetch_users_movies(i[0])
        count = 0
        total_count = genre_weight[str(i[0])]
        for result in results:
            if result not in filtered_results and count <= total_count and result['id'] not in watched_movies_id:
                filtered_results.append(result)
                count = count + 1
            if count == total_count:
                break;
    print(len(filtered_results))
    for result in filtered_results:
        print(result['original_title'], ' ', result['id'])


def fetch_users_movies(genre_id):
    api_end_point = 'https://api.themoviedb.org/3/discover/movie?api_key=' + FinalVariables.getAPIKey() + \
                    '&language=en-US&sort_by=popularity.desc&include_video=false&page=1&with_genres=' + str(genre_id)
    headers = {}
    response = requests.get(api_end_point, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.content)
        results = data['results']
        return results
    else:
        return 0


def get_search_results(user_id, query):
    encoded_query = urllib.parse.quote(query)
    api_end_point = 'https://api.themoviedb.org/3/search/movie?api_key=' + FinalVariables.getAPIKey() + \
                    '&&language=en-US&page=1&query=' + encoded_query
    headers = {}
    response = requests.get(api_end_point, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.content)
        results = data['results']
        update_user_preferences(user_id, results[0])
        return results
    else:
        return 0


def update_user_preferences(user_id, movie_details):
    percentage_decrease = FinalVariables.get_percentage_decrease_in_genre()
    movie_genre_ids = movie_details['genre_ids']
    user_preferences = database.fetch_users_preferences(conn)
    genre_percentage = {}
    updated_genre_percentage = {}
    for i in user_preferences:
        genre_percentage[i[0]] = i[1]
    for genre_id in movie_genre_ids:
        if genre_id not in genre_percentage.keys():
            genre_percentage[genre_id] = 0
    total_percentage_decreased = 0
    for genre in genre_percentage.keys():
        if genre not in movie_genre_ids:
            updated_genre_percentage[genre] = genre_percentage[genre] - percentage_decrease
            total_percentage_decreased = total_percentage_decreased + percentage_decrease
    for genre in genre_percentage.keys():
        if genre in movie_genre_ids:
            updated_genre_percentage[genre] = round(genre_percentage[genre] + total_percentage_decreased/len(movie_genre_ids), 2)
    for genre in updated_genre_percentage:
        database.upsert_user_preference(conn, user_id, genre, updated_genre_percentage[genre])
    print('done')


get_search_results('1234', 'The lion king')
