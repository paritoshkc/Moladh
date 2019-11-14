import requests
import json
import database
import FinalVariables
import urllib.parse
import operator


database = database.Database()
conn = database.createConnection()


class MovieDetails:
    """----------------------------------------------------------------------
    Wrapper class structure for parsing json to html frontend
    ----------------------------------------------------------------------"""
    def __init__(self, title, movie_id, movie_rating, overview, release_date, adult, poster_path, genre_ids):
        self.original_title = title
        self.id = movie_id
        self.rating = movie_rating
        self.overview = overview
        self.release_date = release_date
        self.adult = adult
        self.poster_path = poster_path
        self.genre_ids = genre_ids


def user_watches_movie(user_id, movie_details, like):
    """----------------------------------------------------------------------
    Function to update user_preference and users_movies_watched once the
    user has watched the movie
    ----------------------------------------------------------------------"""
    database.input_movie_watched(conn, user_id, movie_details['id'], like)
    update_user_preferences(user_id, movie_details)


def fetch_movies_for_user(user_id):
    """----------------------------------------------------------------------
    Function to fetch, filter and sort genre wise movies for the current logged in user as
    per the user_preferences.
    ----------------------------------------------------------------------"""
    user_watched_movies = database.fetch_users_watched_movies(conn, user_id)
    watched_movies_id = []
    for i in user_watched_movies:
        watched_movies_id.append(i[0])
    no_of_movies = FinalVariables.get_number_of_movies_to_be_displayed()
    user_genre_preferences = database.fetch_users_preferences(conn, user_id)
    genre_weight = {}
    for i in user_genre_preferences:
        weight = (i[1] * no_of_movies) / 100
        genre_weight[str(i[0])] = round(weight)
    filtered_results = []
    for i in user_genre_preferences:
        results = fetch_movies_by_genre(i[0])
        count = 0
        total_count = genre_weight[str(i[0])]
        for result in results:
            if result not in filtered_results and count <= total_count and result['id'] not in watched_movies_id:
                filtered_results.append(result)
                count = count + 1
            if count == total_count:
                break
    filtered_result_objects = []
    for result in filtered_results:
        movie_object = MovieDetails(result['original_title'], result['id'], result['vote_average'], result['overview'],
                                    result['release_date'], result['adult'], result['poster_path'], result['genre_ids'])
        filtered_result_objects.append(movie_object)
    return filtered_result_objects


def fetch_movies_by_genre(genre_id):
    """----------------------------------------------------------------------
    Function to fetch genre wise movies.
    ----------------------------------------------------------------------"""
    api_end_point = 'https://api.themoviedb.org/3/discover/movie?api_key=' + FinalVariables.get_api_key() + \
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
    """----------------------------------------------------------------------
    Function to fetch movies based on the search query of the user.
    ----------------------------------------------------------------------"""
    encoded_query = urllib.parse.quote(query)
    api_end_point = 'https://api.themoviedb.org/3/search/movie?api_key=' + FinalVariables.get_api_key() + \
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
    """----------------------------------------------------------------------
    Function to update genre weights of the user as per the genres of the
    movie
    ----------------------------------------------------------------------"""
    percentage_decrease = FinalVariables.get_percentage_decrease_in_genre()
    movie_genre_ids = movie_details['genre_ids']
    user_preferences = database.fetch_users_preferences(conn, user_id)
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
            if genre_percentage[genre] >= percentage_decrease:
                updated_genre_percentage[genre] = genre_percentage[genre] - percentage_decrease
                total_percentage_decreased = total_percentage_decreased + percentage_decrease
            else:
                current_percentage_decrease = genre_percentage[genre]
                updated_genre_percentage[genre] = 0
                total_percentage_decreased = total_percentage_decreased + current_percentage_decrease
    for genre in genre_percentage.keys():
        if genre in movie_genre_ids:
            updated_genre_percentage[genre] = round(genre_percentage[genre] +
                                                    total_percentage_decreased/len(movie_genre_ids), 2)
    for genre in updated_genre_percentage:
        database.upsert_user_preference(conn, user_id, genre, updated_genre_percentage[genre])
    print(movie_genre_ids)
    print(genre_percentage)
    print(updated_genre_percentage)


def find_similar_users(user_id):
    """----------------------------------------------------------------------
    Function to find similar users of the user
    ----------------------------------------------------------------------"""
    all_users_preferences = database.fetch_all_users_preferences(conn)
    user_preferences = database.fetch_users_preferences(conn, user_id)
    current_user_preferences = {}
    for i in user_preferences:
        current_user_preferences[i[0]] = i[1]
    user_data_dictionary = {}
    for i in all_users_preferences:
        if i[0] in user_data_dictionary.keys():
            data = user_data_dictionary[i[0]]
            data[i[1]] = i[2]
            user_data_dictionary[i[0]] = data
        else:
            data = {i[1]: i[2]}
            user_data_dictionary[i[0]] = data
    similar_user_scores = {}
    for i in user_data_dictionary.keys():
        user_preference = user_data_dictionary[i]
        difference = 0
        for current_key in current_user_preferences.keys():
            if current_key in user_preference.keys():
                difference = difference + abs(current_user_preferences[current_key] - user_preference[current_key])
            else:
                difference = difference + current_user_preferences[current_key]
        similar_user_scores[i] = round(difference, 2)
    sorted_user_scores = sorted(similar_user_scores.items(), key=operator.itemgetter(1))
    return sorted_user_scores


def get_similar_user_movies(user_id):
    """----------------------------------------------------------------------
    Function to fetch movies watched by the similar user
    ----------------------------------------------------------------------"""
    similar_users = find_similar_users(user_id)
    most_similar_user_id = similar_users[1][0]
    current_user_movies = database.fetch_users_watched_movies(conn, user_id)
    user_movies = []
    for current_user_movie in current_user_movies:
        user_movies.append(current_user_movie[0])
    similar_user_movies = database.fetch_users_watched_movies(conn, most_similar_user_id)
    recommended_movies = []
    similar_user_liked_movies = []
    for similar_user_movie in similar_user_movies:
        if similar_user_movie[1] == 1:
            similar_user_liked_movies.append(similar_user_movie[0])
    for similar_movie in similar_user_liked_movies:
        if similar_movie not in user_movies:
            recommended_movies.append(similar_movie)
    similar_users_movies_objects = []
    count = 0
    max_count = FinalVariables.get_number_of_similar_user_movies()
    for recommended_movie in recommended_movies:
        api_end_point = 'https://api.themoviedb.org/3/movie/' + str(recommended_movie) + '?api_key=' + \
                        FinalVariables.get_api_key() + '&language=en-US'
        headers = {}
        response = requests.get(api_end_point, headers=headers)
        if response.status_code == 200:
            count = count + 1
            data = json.loads(response.content)
            genres = data['genres']
            genres_ids = []
            for genre in genres:
                genres_ids.append(genre['id'])
            movie_object = MovieDetails(data['original_title'], data['id'], data['vote_average'], data['overview'],
                                        data['release_date'], data['adult'], data['poster_path'], genres_ids)
            similar_users_movies_objects.append(movie_object)
            if count == max_count:
                break
    return similar_users_movies_objects


def get_interested_in_movies_for_user(user_id):
    """----------------------------------------------------------------------
    Function to fetch interested in movies for the user.
    ----------------------------------------------------------------------"""
    current_user_movies = database.fetch_users_watched_movies(conn, user_id)
    user_movies = []
    for current_user_movie in current_user_movies:
        user_movies.append(current_user_movie[0])
    count = 0
    max_count = FinalVariables.get_number_of_interested_in_movies()
    interested_in_movies_objects = []
    for user_movie in user_movies:
        api_end_point = 'https://api.themoviedb.org/3/movie/' + str(user_movie) + '/similar?api_key=' + \
                        FinalVariables.get_api_key() + '&language=en-US&page=1'
        headers = {}
        response = requests.get(api_end_point, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.content)
            results = data['results']
            if results[0]['id'] not in user_movies:
                count = count + 1
                movie_object = MovieDetails(results[0]['original_title'], results[0]['id'], results[0]['vote_average'],
                                            results[0]['overview'], results[0]['release_date'], results[0]['adult'],
                                            results[0]['poster_path'], results[0]['genre_ids'])
                interested_in_movies_objects.append(movie_object)
            if count == max_count:
                break
    return interested_in_movies_objects


def get_trending_movies(user_id):
    """----------------------------------------------------------------------
    Function to fetch trending movies for the user
    ----------------------------------------------------------------------"""
    current_user_movies = database.fetch_users_watched_movies(conn, user_id)
    user_movies = []
    for current_user_movie in current_user_movies:
        user_movies.append(current_user_movie[0])
    api_end_point = 'https://api.themoviedb.org/3/trending/movie/day?api_key=' + FinalVariables.get_api_key() + '&page=1'
    headers = {}
    response = requests.get(api_end_point, headers=headers)
    trending_movies_objects = []
    if response.status_code == 200:
        data = json.loads(response.content)
        results = data['results']
        count = 0
        max_count = FinalVariables.get_number_of_trending_movies()
        for result in results:
            if result['id'] not in user_movies:
                count = count + 1
                movie_object = MovieDetails(result['original_title'], result['id'], result['vote_average'],
                                            result['overview'], result['release_date'], result['adult'],
                                            result['poster_path'], result['genre_ids'])
                trending_movies_objects.append(movie_object)
            if count == max_count:
                break
    return trending_movies_objects


def get_recommended_movies_for_user(user_id):
    """----------------------------------------------------------------------
    Function to get all recommended movies for the user
    ----------------------------------------------------------------------"""
    similar_user_movies = get_similar_user_movies(user_id)
    print(len(similar_user_movies))
    trending_movies = get_trending_movies(user_id)
    print(len(trending_movies))
    interested_in_movies = get_interested_in_movies_for_user(user_id)
    print(len(interested_in_movies))
    recommended_movies = similar_user_movies
    for trending_movie in trending_movies:
        if trending_movie not in recommended_movies:
            recommended_movies.append(trending_movie)
    for interested_in_movie in interested_in_movies:
        if interested_in_movie not in recommended_movies:
            recommended_movies.append(interested_in_movie)
    return recommended_movies



#similar_users = find_similar_users('1234')
#print(similar_users)


movies = get_recommended_movies_for_user('1234')
for movie in movies:
    print(movie.id, ' ', movie.original_title)
"""
user_movies = fetch_movies_for_user('1234')
for movie in user_movies:
    print(movie.id, ' ', movie.original_title)
"""
#movies = get_interested_in_movies_for_user('1234')
#print(len(movies))
# fetch_movies_for_user('1236')
# get_search_results('1238', 'Samba')
