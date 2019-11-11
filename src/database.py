import sqlite3
import sys
import os

class Database():
    def readUser(self, conn, username):
        cur=conn.cursor()
        cur.execute("Select ID from User where Username=?",(username,))
        id=cur.fetchall()
        rows=[i[0] for i in id]
        return rows

    def inputUser(self, conn, username, password, adult):
        conn.execute("INSERT INTO User (Username, Password, Adult) VALUES (?, ?, ?);", (username, password, adult))
        conn.commit()

    def input_preferences(self, conn, username, genre):
        conn.execute("INSERT INTO User_Preferences (ID, Genre_ID) VALUES (?, ?);", (username,genre))
        conn.commit()

    def input_movie_watched(self, conn, user_id, movie_id, like):
        conn.execute("INSERT INTO Movies_Watched (ID, MovieID, Like) VALUES (?, ?, ?);", (user_id, movie_id, like))
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
        cur=conn.cursor()
        cur.execute("Select [Genre_Name] from Genres")
        genre_name=cur.fetchall()
        rows=[i[0] for i in genre_name]
        conn.commit()
        return rows

    def readGenreID(self, conn):
        cur=conn.cursor()
        cur.execute("Select ID from Genres")
        genre_ID=cur.fetchall()
        rows=[i[0] for i in genre_ID]
        conn.commit()
        return rows

    def readID_fromGenres(self,conn,genre):
        cur=conn.cursor()
        cur.execute("Select Genre_Name from Genres where ID=?",genre)
        genre_name=cur.fetchall()
        rows=[i[0] for i in genre_name]
        conn.commit()
        return rows 

    def upsert_user_preference(self, conn, user_id, genre_id, percentage):
        cur = conn.cursor()
        query = 'Select count() FROM User_Preferences WHERE ID = ' + str(user_id) + ' AND Genre_Id = ' + str(genre_id)
        cur.execute(query)
        rows = cur.fetchall()
        if rows[0][0] <= 0:
            conn.execute("INSERT INTO User_Preferences (ID, Genre_Id, Percent) VALUES (?, ?, ?);", (user_id, genre_id, percentage))
            conn.commit()
        else:
            query = 'UPDATE User_Preferences SET Percent = ' + str(percentage) + \
                    ' WHERE ID = ' + str(user_id) + ' AND Genre_Id = ' + str(genre_id)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()


    def createConnection(self):
        conn = sqlite3.connect("src\Moladh.db")
        return conn


    def fetch_users_preferences(self, conn, user_id):
        cur = conn.cursor()
        query = 'Select Genre_Id, Percent FROM User_Preferences WHERE ID = ' + str(user_id)
        cur.execute(query)
        rows = cur.fetchall()
        return rows


    def fetch_all_users_preferences(self, conn):
        cur = conn.cursor()
        cur.execute("Select ID, Genre_Id, Percent FROM User_Preferences")
        rows = cur.fetchall()
        return rows


    def fetch_users_watched_movies(self, conn):
        cur = conn.cursor()
        cur.execute("Select MovieID FROM Movies_Watched")
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