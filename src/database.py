import sqlite3
from datetime import date
import sys
import os


class Database():
    def readUser(self, conn, username):
        cur = conn.cursor()
        cur.execute("Select ID from User where Username=?", (username,))
        id = cur.fetchall()
        rows = [i[0] for i in id]
        return rows


    def checkUser(self, conn, username, password):
        cur = conn.cursor()
        cur.execute("Select Password from User where Username=?", (username,))
        rows = cur.fetchall()
        password_db = [i[0] for i in rows]
        if password_db[0] == password:
            return True
        else:
            return False

    def inputUser(self, conn, username, password, adult):
        conn.execute("INSERT INTO User (Username, Password, Adult) VALUES (?, ?, ?);", (username, password, adult))
        conn.commit()

    def input_preferences(self, conn, username, genre, percent):
        conn.execute("INSERT INTO User_Preferences (ID, Genre_ID,percent) VALUES (?, ?, ?);",
                     (username, genre, percent))
        conn.commit()


    def upsert_movie_watched(self, conn, user_id, movie_id, like, dislike, watched):
        today = date.today()
        cur = conn.cursor()
        query = 'Select count() FROM Movies_Watched WHERE ID = ' + str(user_id) + ' AND MovieID = ' + str(movie_id)
        cur.execute(query)
        rows = cur.fetchall()
        if rows[0][0] <= 0:
            conn.execute("INSERT INTO Movies_Watched (ID, MovieID, Like, Date_Watched, Dislike, Watched) VALUES (?, ?, ?, ?, ?, ?);", (user_id, movie_id, like, today, 0, watched))
            conn.commit()
        else:
            query = 'UPDATE Movies_Watched SET Like = ' + str(like) + ', Watched =' + str(watched) + ', Dislike =  ' +\
                    str(dislike) + ' WHERE ID = ' + str(user_id) + ' AND MovieID = ' + str(movie_id)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()

    def input_genre(self, conn, ID, Genre_Name):
        cur = conn.cursor()
        query = 'Select count() FROM Genres WHERE ID = ' + str(ID)
        cur.execute(query)
        rows = cur.fetchall()
        if rows[0][0] <= 0:
            conn.execute("INSERT INTO Genres (ID, Genre_Name) VALUES (?, ?);", (ID, Genre_Name))
            conn.commit()

    def readGenre(self, conn):
        cur = conn.cursor()
        cur.execute("Select [Genre_Name] from Genres")
        genre_name = cur.fetchall()
        rows = [i[0] for i in genre_name]
        conn.commit()
        return rows

    def readGenreID(self, conn):
        cur = conn.cursor()
        cur.execute("Select ID from Genres")
        genre_ID = cur.fetchall()
        rows = [i[0] for i in genre_ID]
        conn.commit()
        return rows

    def readID_fromGenres(self, conn, genre):
        cur = conn.cursor()
        cur.execute("Select Genre_Name from Genres where ID= " + str(genre))
        genre_name = cur.fetchall()
        rows = [i[0] for i in genre_name]
        conn.commit()
        return rows

    def upsert_user_preference(self, conn, user_id, genre_id, percentage):
        cur = conn.cursor()
        query = 'Select count() FROM User_Preferences WHERE ID = ' + str(user_id) + ' AND Genre_Id = ' + str(genre_id)
        cur.execute(query)
        rows = cur.fetchall()
        if rows[0][0] <= 0:
            conn.execute("INSERT INTO User_Preferences (ID, Genre_Id, Percent) VALUES (?, ?, ?);",
                         (user_id, genre_id, percentage))
            conn.commit()
        else:
            query = 'UPDATE User_Preferences SET Percent = ' + str(percentage) + \
                    ' WHERE ID = ' + str(user_id) + ' AND Genre_Id = ' + str(genre_id)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()


    def createConnection(self):
        conn = sqlite3.connect("src/Moladh.db", check_same_thread=False)
        return conn


    def fetch_users_preferences(self, conn, user_id):
        cur = conn.cursor()
        query = 'Select Genre_Id, Percent FROM User_Preferences WHERE ID = ' + str(user_id)
        cur.execute(query)
        rows = cur.fetchall()
        return rows


    def fetch_users_unwatched_movies(self, conn, user_id, days):
        cur = conn.cursor()
        query = 'Select ID, MovieID FROM Movies_Watched WHERE ID = ' + str(user_id) + ' AND Watched = 0' + \
                ' AND Dislke = 0 AND Date_Watched >= (SELECT date(\'now\', \'' + str(-1 * days) + ' day\'))'
        cur.execute(query)
        rows = cur.fetchall()
        return rows


    def fetch_all_users_preferences(self, conn):
        cur = conn.cursor()
        cur.execute("Select ID, Genre_Id, Percent FROM User_Preferences")
        rows = cur.fetchall()
        return rows

    def fetch_users_watched_movies(self, conn, user_id):
        cur = conn.cursor()
        query = 'Select MovieID, Like, Dislike, Watched, Date_Watched FROM Movies_Watched WHERE ID = ' + \
                str(user_id) + ' ORDER By Date_Watched DESC'
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def createTables(self, conn):
        conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS User
                (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT,
                    Password TEXT,
                    Adult BOOL
                );
            '''
        )

        conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS Movies_Watched
                (
                    ID INTEGER,
                    MovieID INTEGER,
                    Like BOOL,
                    Date DATE,
                    FOREIGN KEY(ID) REFERENCES User(ID)
                );
            '''
        )

        conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS User_Preferences
                (
                    ID INTEGER,
                    Genre_Id INTEGER,
                    Percent INTEGER,
                    FOREIGN KEY(ID) REFERENCES User(ID)
                );
            '''
        )

        conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS Genres
                (
                    ID INTEGER,
                    Genre_Name TEXT
                );
            '''
        )

        """
        conn.execute(
            '''
                ALTER TABLE Movies_Watched
                ADD COLUMN Watched BOOL
            '''
        )
        """


        conn.commit()


def main():
    database = Database()
    conn = database.createConnection()
    database.createTables(conn)
    print('Tables created')


if __name__ == "__main__":
    main()

"""
def main():
    conn = sqlite3.connect("Moladh")
    inp = input("Enter 1 -> Create tables  2 -> Input users  3 -> Input movie watched  any_other_key -> Exit : ")
    if inp == "1":
        createTables(conn)

    elif inp == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        adult = input("Are you an adult? [1/0]: ")
        inputUser(conn, username, password, adult)

    elif inp == "3":
        ID = input("Enter user ID: ")
        movieID = input("Enter movie ID: ")
        Like = input("Did you like the movie [1/0]: ")
        inputMovieWatched(conn, ID, movieID, Like)

    else:
        conn.commit()
        conn.close()
        sys.exit()

"""
