import mysql.connector


name = input('Please Enter the Fencers name: ')
dob = input('Please Enter Fencers Date of Birth: ')
ranking =  input('Please Enter the fencers ranking')
club = input('Please enter the fencers club')

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Combated12"
    database = "words")

mycursor = mydb.cursor()

mycursor.excute("SHOW TABLES")