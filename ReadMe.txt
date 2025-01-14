RideShare Program

A simple Python-based ride-sharing application that interacts with a MySQL database. Users can register as drivers or riders, request rides, view ride history, and provide driver ratings.

Requirements
1. Python 3.8+
2. MySQL Server
3. MySQL Connector for Python
   pip install mysql-connector-python
4. A MySQL database named RideShare (or update the code with your own database name/credentials).

Setup Instructions
1. Clone or download the program to your local system.
2. Create the MySQL database:
   CREATE DATABASE RideShare;
3. Set up the required tables:
   USE RideShare;

   CREATE TABLE Driver (
     DriverID INT PRIMARY KEY,
     Name VARCHAR(255),
     Date_of_Birth DATE,
     Activity_Status BOOLEAN
   );

   CREATE TABLE Rider (
     RiderID INT PRIMARY KEY,
     Name VARCHAR(255),
     Date_of_Birth DATE
   );

   CREATE TABLE Rides (
     RideID INT PRIMARY KEY,
     DriverID INT,
     RiderID INT,
     Pick_Up_Location VARCHAR(255),
     Drop_Off_Location VARCHAR(255),
     Customer_Rating FLOAT
   );
4. Update MySQL credentials in the main() function of the Python file:
   conn = mysql.connector.connect(
       host="localhost",
       user="root",
       password="CPSC_408!",
       auth_plugin='mysql_native_password',
       database="RideShare"
   )
   (Modify host, user, password, and database as per your MySQL setup.)

How to Run
1. Open a terminal and navigate to the directory containing the program file.
2. Run the program:
   python rideshare_app.py
3. Follow the on-screen prompts to:
   - Register as a new user (driver or rider) or log in as a returning user.
   - Perform actions based on your user type:
     Rider: Request rides, view ride history, or rate drivers.
     Driver: View rides given, check average rating, or toggle availability.

Program Features
1. New User Registration:
   Register as a rider or driver with basic information (name and date of birth).
2. Returning User Login:
   Log in using your user ID and view your details.
3. Ride Management:
   Riders can request rides (if drivers are available) and view past rides.
   Drivers can view rides they've given and toggle their availability.
4. Driver Ratings:
   Riders can rate drivers, and the program calculates an average driver rating.

Troubleshooting
- If tables do not exist, create them manually using the SQL commands provided in the setup section.
- Ensure MySQL is running and the credentials in the main() function match your setup.
- Install missing dependencies with:
   pip install mysql-connector-python

License
This program is open-source. Feel free to use, modify, and share it.
