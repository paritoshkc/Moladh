from flask import *
import database
import Backend as be
from datetime import datetime
import secrets
from operator import itemgetter

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

database = database.Database()
conn = database.createConnection()
# database.createTables(conn)
genre = database.readGenre(conn)
genre_ID = database.readGenreID(conn)


def calculateAge(birthDate):
    today = datetime.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def fetch_movies():
    movie_details = be.fetch_movies_for_user(session.get("USER_ID")[-1])
    movie_id = []
    movie_title = []
    movie_poster = []
    movie_genres = []
    genre_name = []
    combine_id=[]
    for i in movie_details:
        movie_id.append(i.id)
        movie_title.append(i.original_title)
        movie_poster.append(i.poster_path)
        movie_genres.append(i.genre_ids)
        combine_id.append(str(i.genre_ids)+'&&'+str(i.id))
    length = len(movie_genres)
    for k in range(length):
        genres = []
        for j in movie_genres[k]:
            genres.append(database.readID_fromGenres(conn, j))
        genre_name.append(genres)
    #combine_id=str(movie_genres[0])+'&&'+str(movie_id[0])
    return movie_id,movie_title,movie_poster,movie_genres,genre_name,combine_id

def fetch_user_might_like_movies():
    movie_details = be.get_recommended_movies_for_user(session.get("USER_ID")[-1])
    movie_id = []
    movie_title = []
    movie_poster = []
    movie_genres = []
    genre_name = []
    combine_id=[]
    for i in movie_details:
        movie_id.append(i.id)
        movie_title.append(i.original_title)
        movie_poster.append(i.poster_path)
        movie_genres.append(i.genre_ids)
        combine_id.append(str(i.genre_ids)+'&&'+str(i.id))
    length = len(movie_genres)
    for k in range(length):
        genres = []
        for j in movie_genres[k]:
            genres.append(database.readID_fromGenres(conn, j))
        genre_name.append(genres)
        print(movie_poster[0])
    return movie_title,movie_poster,combine_id

def fetch_continue_watch_movies():
    movie_details = be.get_continue_watching_movies_for_user(session.get("USER_ID")[-1])
    movie_id = []
    movie_title = []
    movie_poster = []
    movie_genres = []
    genre_name = []
    combine_id=[]
    for i in movie_details:
        movie_id.append(i.id)
        movie_title.append(i.original_title)
        movie_poster.append(i.poster_path)
        movie_genres.append(i.genre_ids)
        combine_id.append(str(i.genre_ids)+'&&'+str(i.id))
    length = len(movie_genres)
    for k in range(length):
        genres = []
        for j in movie_genres[k]:
            genres.append(database.readID_fromGenres(conn, j))
        genre_name.append(genres)
    return movie_title,movie_poster,combine_id

def get_search_movies(url):
    search_details=be.get_search_results(session.get("USER_ID")[-1],url)
    movie_id = []
    movie_title = []
    movie_poster = []
    movie_genres = []
    genre_name = []
    combine_id=[]
    for i in search_details:
        movie_id.append(i.id)
        movie_title.append(i.original_title)
        movie_poster.append(i.poster_path)
        movie_genres.append(i.genre_ids)
        combine_id.append(str(i.genre_ids)+'&&'+str(i.id))
    length = len(movie_genres)
    for k in range(length):
        genres = []
        for j in movie_genres[k]:
            genres.append(database.readID_fromGenres(conn, j))
        genre_name.append(genres)
    return movie_title,movie_poster,combine_id
 

@app.route('/')
def hello():
    return render_template("LoginPage.html")

@app.route('/login')
def login():
    return render_template("LoginPage.html")


@app.route('/registration')
def reg():
    return render_template("registration-page.html")

#
# @app.route('/hello', methods=['POST'])
# def register():
#     if request.method == 'POST':
#
#         req = request.form
#
#         username = req.get('username')
#         password = req.get('password')
#
#         if username and database.checkUser(conn, username, password):
#             session["USERNAME"] = username
#             session["USER_ID"] = database.readUser(conn, username)
#             # return render_template('home-page.html', username = username)
#             movie_id,movie_title,movie_poster,movie_genres,genre_name,combine_id=fetch_movies()
#             might_like_title,might_like_poster,might_like_id=fetch_user_might_like_movies()
#             continue_watch_title,continue_watch_poster,continue_watch_id=fetch_continue_watch_movies()
#             return render_template('ff.html', movie_id=movie_id, movie_title=movie_title, movie_poster=movie_poster,
#                            movie_genres=genre_name,might_like_title=might_like_title,might_like_poster = might_like_poster,continue_watch_title= continue_watch_title
#                            ,continue_watch_poster=continue_watch_poster,might_like_id=might_like_id,continue_watch_id=continue_watch_id,combine_id=combine_id)
#
#         else:
#             return render_template('login-page.html')

@app.route('/hello', methods=['POST'])
def register1():
    if request.method == 'POST':

        req = request.form

        username = req.get('username')
        password = req.get('password')

        if username and database.checkUser(conn, username, password):
            session["USERNAME"] = username
            session["USER_ID"] = database.readUser(conn, username)
            # return render_template('home-page.html', username = username)
            movie_id, movie_title, movie_poster, movie_genres, genre_name, combine_id = fetch_movies()
            might_like_title, might_like_poster, might_like_id = fetch_user_might_like_movies()
            continue_watch_title, continue_watch_poster, continue_watch_id = fetch_continue_watch_movies()
            return render_template('movie-page.html', poster_id_title=zip(combine_id,movie_title,movie_poster),might_id_title_poster=zip(might_like_id,might_like_title,might_like_poster),continue_id_title_poster=zip(continue_watch_id,continue_watch_title,continue_watch_poster))

        else:
         return render_template('LoginPage.html',msg="Wrong Username or Password")


@app.route('/registered', methods=['POST'])
def welcome():
    req = request.form

    user = req.get('reg_username')
    password = req.get('reg_password')
    gender = req.get('reg_gender')
    # nationality = request.form['nationality']
    # email = request.form['email']
    dob = req.get('dob')
    # if the user is adult or not
    adult = False
    if calculateAge(datetime.strptime(dob, '%Y-%m-%d')) > 18:
        adult = True

    # connection
    #database = database.Database()

    con = database.createConnection()
    # database.createTables(con)
    database.inputUser(con, user, password, adult)
    username = database.readUser(con, user)
    session["USERNAME"] = user
    session["USER_ID"] = username
    return render_template('Genre-selection.html' ,name_id=zip(genre,genre_ID))


@app.route('/genre_page', methods=['POST'])
def genre_section():
    # user = request.form['username']
    con_genre = database.createConnection()
    # database.createTables(con_genre)s
    checkboxes = request.form.getlist('check')
    test_arr = []
    genre_name = []
    total_genres = len(checkboxes)
    percent = []
    i = 0
    for check in checkboxes:
        test_arr.append(str(check))
        percent.append(round((100 / total_genres), 2))
        print(test_arr)
        # id=database.readGenreID(con_genre,test_arr[i])
        print(session)
        database.input_preferences(conn=con_genre, username=session.get("USER_ID")[-1], genre=test_arr[i],
                                   percent=percent[i])
        i = i + 1
    # print(user_set)
    movie_id,movie_title,movie_poster,genre_id,genre_name,combine_id=fetch_movies()
    might_like_title,might_like_poster,might_like_id=fetch_user_might_like_movies()
    continue_watch_title,continue_watch_poster,continue_watch_id=fetch_continue_watch_movies()
    return render_template('movie-page.html',poster_id_title=zip(combine_id,movie_title,movie_poster),might_id_title_poster=zip(might_like_id,might_like_title,might_like_poster),continue_id_title_poster=zip(continue_watch_id,continue_watch_title,continue_watch_poster))


@app.route('/select-page',methods=['POST'])
def get_search_result():
    url = request.form['url']
    #r = requests.get(url)
    print(url)
    get_search_movies(url)
    name,poster,id=get_search_movies(url)
    return render_template('search-page.html',name_poster_id=zip(name,poster,id))


# @app.route('',)
@app.route('/movie_watched/<mw>/<ml>/<mid>', methods=['POST'],)
def movie_watched(mw,ml,mid):

    mw = (mw == '1')
    ml = (ml == '1')
    mid=mid
    be.user_watches_movie(session.get("USER_ID")[-1], mid,ml,mw)
    print(mw,ml,mid)

    return ('hi')



@app.route('/check_user', methods=['POST'])
def print_user_details():
    if request.method == 'POST':
        if request.form['username'] != "":
            username = request.form['username']
            password = request.form['password']
        return render_template('user_home.html', username=username, password=password)


@app.route('/popup', methods=['GET'])
def popup():
    return render_template('loading_page.html')


if __name__ == '__main__':
    app.run()
