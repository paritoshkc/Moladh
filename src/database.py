import sqlite3
import sys
import os

class Database():

    def inputUser(self, conn, username, password, adult):
        conn.execute("INSERT INTO User (Username, Password, Adult) VALUES (?, ?, ?);", (username, password, adult))
        conn.commit()

    def inputMovieWatched(self, conn, ID, movieID, Like):
        conn.execute("INSERT INTO Movies_Watched (ID, MovieID, Like) VALUES (?, ?, ?);", (ID, movieID, Like))
        conn.commit()

    def createGenre(self, conn, ID, genre):
        conn.execute("INSERT INTO Genres (ID, Genre_Name) VALUES (?, ?);", (ID, genre))
        conn.commit()

    def createConnection(self):
        print('testing')
        os.chdir("../DB")
        conn = sqlite3.connect("Moladh.db")
        os.chdir("../src")
        return conn

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
