import mysql.connector

def createTables(conn, cur_obj):
    cur_obj.execute('''
    CREATE TABLE Rider(
        RiderID INT NOT NULL PRIMARY KEY,
        Name VARCHAR(40) NOT NULL,
        Date_of_Birth DATE NOT NULL
    );
    ''')


    cur_obj.execute('''
    CREATE TABLE Driver(
        DriverID INT NOT NULL PRIMARY KEY,
        Name VARCHAR(40) NOT NULL,
        Date_of_Birth DATE NOT NULL,
        Activity_Status BOOL NOT NULL
    );
    ''')

def createRides(conn, cur_obj):
    cur_obj.execute('''
    CREATE TABLE Rides(
        RideID INT NOT NULL PRIMARY KEY,
        DriverID INT NOT NULL,
        RiderID INT NOT NULL,
        Pick_Up_Location VARCHAR(50) NOT NULL,
        Drop_Off_Location VARCHAR(50) NOT NULL,
        Customer_Rating DOUBLE
    );
    ''')
    #DriverID = Foreign Key
    #RiderID = Foreign Key
    print("Tables Created!")

def deleteTables(conn, cur_obj):
    cur_obj.execute('''
    DROP TABLE Rides
    ''')

    #cur_obj.execute('''
    #DROP TABLE Rider
    #''')

    #cur_obj.execute('''
    #DROP TABLE Driver
    #''')

def insertNewDriver(conn, cur_obj, userName, birthDate, ActivityStatus):
    count_query = 'SELECT COUNT(*) FROM Driver;'
    cur_obj.execute(count_query)
    count = cur_obj.fetchone()[0]

    DriverID = count

    insert_query = '''
    INSERT INTO Driver (DriverID, Name, Date_of_Birth, Activity_Status)
    VALUES (%s, %s, %s, %s);
    '''
    values = (DriverID, userName, birthDate, ActivityStatus)

    cur_obj.execute(insert_query, values)
    print("Driver added successfully")
    return DriverID

def returnDriverName(conn, cur_obj, userID):
    query = 'SELECT Name FROM Driver WHERE DriverID = %s;'
    
    cur_obj.execute(query, (userID,))
    
    result = cur_obj.fetchone()
    
    if result:
        return result[0]

def returnRiderName(conn, cur_obj, userID):
    query = 'SELECT Name FROM Rider WHERE RiderID = %s;'
    
    cur_obj.execute(query, (userID,))
    
    result = cur_obj.fetchone()
    
    if result:
        return result[0]

def returnDriverID(conn, cur_obj, userName):
    query = 'SELECT Name FROM Driver WHERE Name = %s;'
    
    cur_obj.execute(query, (userName,))
    
    result = cur_obj.fetchone()
    
    if result:
        return result[0]

def returnRiderID(conn, cur_obj, userName):
    query = 'SELECT Name FROM Rider WHERE Name = %s;'
    
    cur_obj.execute(query, (userName,))
    
    result = cur_obj.fetchone()
    
    if result:
        return result[0]

def changeActivityStatus(conn, cur_obj, userID):
    select_query = 'SELECT Activity_Status FROM Driver WHERE DriverID = %s'
    cur_obj.execute(select_query, (userID,))
    result = cur_obj.fetchone()

    if result:
        activity_status = result[0]
        
        if activity_status:
            update_query = 'UPDATE Driver SET Activity_Status = FALSE WHERE DriverID = %s'
            cur_obj.execute(update_query, (userID,))
            conn.commit()
            print("Activity status updated to False")
        else:
            update_query = 'UPDATE Driver SET Activity_Status = True WHERE DriverID = %s'
            cur_obj.execute(update_query, (userID,))
            conn.commit()
            print("Activity status updated to True")

def insertNewRider(conn, cur_obj, userName, birthDate):
    count_query = 'SELECT COUNT(*) FROM Rider;'
    cur_obj.execute(count_query)
    count = cur_obj.fetchone()[0]

    RiderID = count

    insert_query = '''
    INSERT INTO Rider (RiderID, Name, Date_of_Birth)
    VALUES (%s, %s, %s);
    '''
    values = (RiderID, userName, birthDate)

    cur_obj.execute(insert_query, values)
    print("Rider added successfully")
    return RiderID

def createNewRide(conn, cur_obj, userID):
    driver_query = 'SELECT DriverID FROM Driver WHERE Activity_Status = 1;'
    cur_obj.execute(driver_query)
    result = cur_obj.fetchone()
    if result:
        DriverID = result[0]
        pickUp = input("What is your pick up location? ")
        dropOff = input("What is your drop off location? ")

        count_query = 'SELECT COUNT(*) FROM Rides;'
        cur_obj.execute(count_query)

        count = cur_obj.fetchone()[0]

        RidesID = count

        print("...")
        Rating = int(input("Arrived at "+ dropOff +"! Rate your ride out of 5? "))
        if Rating < 1:
            print("That's not an option")
            Rating = None
        elif Rating > 5:
            print("That's not an option")
            Rating = None
        insert_query = '''
            INSERT INTO Rides (RideID, DriverID, RiderID, Pick_Up_Location, Drop_Off_Location, Customer_Rating)
            VALUES (%s, %s, %s, %s, %s, %s);
            '''
        values = (RidesID, DriverID, userID, pickUp, dropOff, Rating)

        cur_obj.execute(insert_query, values)
        print("Ride added successfully")
    else:
        print("Sorry there are currently no available drivers")

def rateDriver(conn, cur_obj, userID):
    query = '''SELECT *
    FROM Rides
    WHERE RiderID = %s
    ORDER BY RideID DESC
    LIMIT 1;'''
    cur_obj.execute(query, (userID,))
    Ride = cur_obj.fetchone()
    if Ride:
        rideID, driverID, riderID, pickUp, dropOff, currentRating = Ride
        print("Ride details:")
        print(f"RideID: {rideID}")
        print(f"DriverID: {driverID}")
        print(f"RiderID: {riderID}")
        print(f"Pick Up: {pickUp}")
        print(f"Drop Off: {dropOff}")
        print(f"Current Rating: {currentRating}")
        
        correct = int(input("Is this the ride you would like to rate?: [Yes(1) No(0)] "))
    
        if (correct == 1):
            rating = int(input("What would you like to rate this ride out of 5? "))
            rating2 = (currentRating + rating)/2
            if 0 < rating <= 5:
                # Update the rating for the driver
                update_query = 'UPDATE Rides SET Customer_Rating = %s WHERE RideID = %s;'
                cur_obj.execute(update_query, (rating2, rideID))
                conn.commit()
                print("Rating updated!")
        else:
            query = '''SELECT RideID
            FROM Rides
            WHERE RiderID = %s;'''
            cur_obj.execute(query, (userID,))
            ride_ids = cur_obj.fetchall()
            for row in ride_ids:
                print(row[0])
            new_RideID = int(input("Choose the ride ID you would like to rate "))
            if new_RideID in ride_ids[0]:
                rating = int(input("What would you like to rate this ride out of 5? "))
                rating2 = (currentRating + rating)/2
                if 0 < rating <= 5:           
                    update_query = 'UPDATE Rides SET Customer_Rating = %s WHERE RideID = %s;'
                    cur_obj.execute(update_query, (rating2, new_RideID))
                    conn.commit()
                    print("Rating updated!")
            else:
                print("You didn't go on that ride")
    else:
        print("You haven't gone on any rides silly")
def printRiderRides(conn, cur_obj, userID):
    query = '''SELECT * FROM Rides WHERE RiderID = %s'''
    cur_obj.execute(query, (userID,))
    Allrides = cur_obj.fetchall()
    
    for ride in Allrides:
        rideID, driverID, riderID, pickUp, dropOff, currentRating = ride
        print("Ride details:")
        print(f"RideID: {rideID}")
        print(f"DriverID: {driverID}")
        print(f"RiderID: {riderID}")
        print(f"Pick Up: {pickUp}")
        print(f"Drop Off: {dropOff}")
        print(f"Current Rating: {currentRating}")
        print("\n")

def printDriverRides(conn, cur_obj, userID):
    query = '''SELECT * FROM Rides WHERE DriverID = %s'''
    cur_obj.execute(query, (userID,))
    Allrides = cur_obj.fetchall()
    
    for ride in Allrides:
        rideID, driverID, riderID, pickUp, dropOff, currentRating = ride
        print("Ride details:")
        print(f"RideID: {rideID}")
        print(f"DriverID: {driverID}")
        print(f"RiderID: {riderID}")
        print(f"Pick Up: {pickUp}")
        print(f"Drop Off: {dropOff}")
        print(f"Current Rating: {currentRating}")
        print("\n")

def calcDriverRating(conn, cur_obj, userID):
    query = '''SELECT Customer_Rating FROM Rides WHERE DriverID = %s'''
    cur_obj.execute(query, (userID,))
    Allrides = cur_obj.fetchall()
    Total = 0
    for ride in Allrides:
        Total += ride[0]
    Total = Total/(len(Allrides))
    print("Driver Current Rating:", Total)

def main():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CPSC_408!",
        auth_plugin='mysql_native_password',
        database="RideShare"
    )
    cur_obj = conn.cursor()

    userStatus = int(input("Are you a (1) new or (2) returning user? "))
    if userStatus not in [1,2]:
        print("That's not an option.")
        return
    userType = int(input("Are you a (1) rider or (2) a driver? "))
    if userType not in [1,2]:
        print("That's not an option.")
    if (userStatus == 1):
        userName = input("What is your name? ")
        birthYear = input("What year were you born? ")
        birthMonth = input("What month were you born? ")
        birthDay = input("What day were you born? ")
        birthDate = birthYear + "/" + birthMonth + "/" + birthDay
        if (userType == 2):
            ActivityStatus = False
            insertNewDriver(conn, cur_obj, userName, birthDate, ActivityStatus)
            userID = insertNewDriver(conn, cur_obj, userName, birthDate, ActivityStatus)
            conn.commit()
        else:
            userID = insertNewRider(conn, cur_obj, userName, birthDate)
            conn.commit()
        print("Welcome", userName)
    else:
        userID = int(input("Please input you ID number "))
        if(userType == 1):
            print("Welcome", returnRiderName(conn, cur_obj, userID))
        else:
            print("Welcome", returnDriverName(conn, cur_obj, userID))

    while(userType == 1):
        choice = int(input('''Select from the following menu options: 
        1. View Rides
        2. Request Ride
        3. Rate Driver
        4. Exit
        '''))
        if choice == 1:
            print(1)
            printRiderRides(conn, cur_obj, userID)
        elif choice == 2:
            createNewRide(conn, cur_obj, userID)
            conn.commit()
        elif choice == 3:
            print(3)
            rateDriver(conn, cur_obj, userID)
            conn.commit()
        else:
            userType = 3
            print("Bye Bye")
    while(userType == 2):
        choice = int(input('''Select from the following menu options: 
        1. Show Rides
        2. Show Ratings
        3. Active or Deactivate Driver Mode
        Else. Exit
        '''))
        if choice == 1:
            printDriverRides(conn, cur_obj, userID)
        elif choice == 2:
            calcDriverRating(conn, cur_obj, userID)
        elif choice == 3:
            changeActivityStatus(conn, cur_obj, userID)
        else:
            userType = 3
            print("Bye Bye")



main()