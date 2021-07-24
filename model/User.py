from model.DatabasePool import DatabasePool

from config.Settings import Settings
import datetime
import jwt

#hashing password..
#import bcrypt

class User:

    @classmethod
    def getAllUsers(cls):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            sql="select * from user"
            cursor.execute(sql)
            users=cursor.fetchall()

            return users
        
        finally:
            dbConn.close()


    @classmethod
    def getUser(cls,userid):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            sql="select * from user where userid=%s"
            cursor.execute(sql,(userid,))
            users=cursor.fetchall()

            return users
        
        finally:
            dbConn.close()


    @classmethod
    def insertUser(cls,username,email,role,password):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            #hashing password...
            #password=password.encode() #convert string to bytes
            #password = bcrypt.hashpw(password, bcrypt.gensalt())


            sql="insert into user(username,email,role,password) values(%s,%s,%s,%s)"
            cursor.execute(sql,(username,email,role,password))
            dbConn.commit() #for insert/update/delete sql statements

            rows=cursor.rowcount#number of rows added/changed in the database
            print(cursor.lastrowid)

            return rows
        
        finally:
            dbConn.close()

    @classmethod
    def updateUser(cls,email,password,userid):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            sql="update user set email=%s,password=%s where userid=%s"
            cursor.execute(sql,(email,password,userid))
            dbConn.commit() #for insert/update/delete sql statements

            rows=cursor.rowcount#number of rows added/changed in the database

            return rows
        
        finally:
            dbConn.close()


    @classmethod
    def deleteUser(cls,userid):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            sql="delete from user where userid=%s"
            cursor.execute(sql,(userid,))
            dbConn.commit() #for insert/update/delete sql statements

            rows=cursor.rowcount#number of rows added/changed in the database

            return rows
        
        finally:
            dbConn.close()

    @classmethod
    def login(cls,email,password):
        try: 
            dbConn=DatabasePool.getConnection()#get a free connection to the database
            cursor = dbConn.cursor(dictionary=True)

            sql="select * from user where email=%s and password=%s";
            cursor.execute(sql,(email,password));
            users=cursor.fetchall();

            if len(users)==0:
                return {"jwt":""}

            else:
                user=users[0]
                payload={"userid":user["userid"],"role":user["role"],"username":user["username"],"exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}
                key=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                return {"jwt":key}

                    
        finally:
            dbConn.close()