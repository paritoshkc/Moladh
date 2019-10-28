import sqlite3
import sys

def createTables(conn):
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

    conn.commit()
    main()

def inputUser(conn, username, password, adult):
    conn.execute("INSERT INTO User (Username, Password, Adult) VALUES (?, ?, ?);", (username, password, adult))
    conn.commit()
    main()

def inputMovieWatched(conn, ID, movieID, Like):
    conn.execute("INSERT INTO Movies_Watched (ID, MovieID, Like) VALUES (?, ?, ?);", (ID, movieID, Like))
    conn.commit()
    main()

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


if __name__ == "__main__":
    main()