import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import datetime

# loading the data from the .env file
load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

tf_time = ''
if_time = ''
t2i_time = ''
if_id = ''
if_name = ''
tf_id = ''
tf_name = ''
t2i_name = ''
t2i_id = ''

# Current date and time
timenow = datetime.datetime.now()

print('initiating database connection')
strCon = 'host=' + HOST + ' port=' + PORT + ' user=' + USER + ' password=' + PASSWORD + ' database=' + DATABASE
print(strCon)
try:
    mydb = mysql.connector.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    mydb.autocommit = True
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SET SESSION MAX_EXECUTION_TIME=3000")
    print('database connection successful')

    # Inserting data into the database    *********This is the part I need help with********* to slect the data sources
    Add_thermalfeed = ("INSERT INTO `thermalfeed` (`TF_ID`, `Name`, `Date`,`ImageData1`) VALUES (%s, %s, %s, %s, %s)")
    Add_imagefeed = ("INSERT INTO `imagefeed` (`IF_ID`, `Name`, `Date`,`ImageData2`) VALUES (%s, %s, %s, %s, %s)")

    # Have to join the both thermal feed and image feed data to form the thermal2imagelink table
    Add_thermal2image = (
        "INSERT INTO `thermal2image` (`TI_ID`, `Name`,`Date` ,`TF_ID`,`IF_ID`) VALUES (%s, %s, %s, %s, %s)")

    # Data flow-----> where the data is coming from
    data_thermalfeed = ('tf_id', 'tf_name', 'tf_time', 'tf_data')
    data_imagefeed = ('if_id', 'if_name', 'if_time', 'if_data')
    data_thermal2image = ('t2i_id', 't2i_name', 't2i_time', 'tf_id', 'if_id')

    # Inserting data in to database
    mycursor.execute(Add_thermalfeed, data_thermalfeed)
    tf_id = mycursor.lastrowid
    mycursor.execute(Add_imagefeed, data_imagefeed)
    if_id = mycursor.lastrowid
    mycursor.execute(Add_thermal2image.feed, data_thermal2image)
    t2i_id = mycursor.lastrowid

    # Make sure data is committed to the database
    mydb.commit()
    mycursor.close()
    mydb.close()
    print('data inserted successfully!')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Please check your username or password!")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    mydb.close()
