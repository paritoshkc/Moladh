import random
import sqlite3


class userPreference:
    userID = 0
    genreId = 0
    percentage = 0.0


conn = sqlite3.connect('Moladh.db')

# create the 20 userIDs

userIDs = []

c = conn.cursor()
cursor = c.execute("SELECT ID from User")

for row in cursor:
    if 1299 < row[0] < 1320:
        userIDs.append(row[0])

# create the genreID list

genreIDs = []

cursor = c.execute("SELECT ID from Genres")

for row in cursor:
    genreIDs.append(row[0])


def getGenreIDs():
    conn = sqlite3.connect('Moladh.db')

    c = conn.cursor()

    genreIDs = []

    cursor = c.execute("SELECT ID from Genres")

    for row in cursor:
        genreIDs.append(row[0])

    return genreIDs



# create userPreferences

userPreferences = []

for userID in userIDs:

    userPref = userPreference()

    # the current user has genreNum genre preferences
    genreNum = random.randint(0, 15)
    percentageTotal = 100
    genreIDs_temp = getGenreIDs()
    #print('\n',len(genreIDs_temp),',', len(genreIDs),'\n')

    for i in range(1, genreNum + 1):
        userPref = userPreference()

        print('i= ',i)
        if percentageTotal > 0:

            currentChosenGenreIndex = random.randint(0, len(genreIDs_temp) - 1)
            print(currentChosenGenreIndex, '%%%%%%%', len(genreIDs_temp))

            currentChosenGenreID = genreIDs_temp[currentChosenGenreIndex]
            genreIDs_temp.remove(currentChosenGenreID)

            if i == genreNum:
                userPref.genreId = currentChosenGenreID
                userPref.percentage = round(percentageTotal, 3)
                userPref.userID = userID
                userPreferences.append(userPref)
                break

            # if not the last genre
            if i != genreNum:
                currentPercentage = round(random.uniform(0, percentageTotal), 3)
                print(currentPercentage)
                percentageTotal = percentageTotal - currentPercentage

                userPref.genreId = currentChosenGenreID
                userPref.userID = userID
                userPref.percentage = currentPercentage

                userPreferences.append(userPref)





#put the user preferences into the database

for userPreference in userPreferences:

    c.execute("INSERT INTO User_Preferences (ID, Genre_ID,percent) VALUES (?, ?, ?);",(userPreference.userID, userPreference.genreId, userPreference.percentage))
    #print(userPreference.userID, userPreference.genreId, userPreference.percentage)
conn.commit()
