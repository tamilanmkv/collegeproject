import mysql.connector


mydb = mysql.connector.connect(
    host="lin-2550-2638-mysql-primary.servers.linodedb.net",
    user="linroot",
    passwd="wgghNd0PB4h-zie1",
    database="find"
)

mycursor = mydb.cursor()
# delete all data
#mycursor.execute("DELETE FROM findV")
#mydb.commit()
#mydb.close()
# insert data
#mycursor.execute("INSERT INTO findV(Vehno,Location) VALUES('12345','Bangalore')")
#res = "tn38z2332"
#mycursor.execute("update findV set Latitude = '9.854980',Longitude = '78.500504' where Vehno = %s",(res,))
#mydb.commit()
mycursor.execute("SELECT * FROM findV")
myresult = mycursor.fetchall()
print(myresult)
# create table from find database
#mycursor.execute("")
#mycursor.commit()
#mycursor.execute("CREATE TABLE findBlock(Vehno varchar(50),Location VARCHAR(255),latitude VARCHAR(255),longitude VARCHAR(255));")
#mycursor.execute("insert into findBlock(Vehno,Location,latitude,longitude) values('12345','Bangalore','9.854980','78.500504')")
#mycursor.execute('create table blockNO(vno varchar(10))')
#mycursor.execute('insert into blockNO(vno) values("tn38z2332")')
#mydb.commit()
mycursor.execute("SELECT * FROM blockNO")
myresult = mycursor.fetchall()
#print(myresult)
#mycursor.execute('insert into blockNO(vno) values("tn38z2332")')
#mycursor.execute('insert into blockNO(vno) values("tn38z2332")')
#mycursor.execute('insert into blockNO(vno) values("tn38z2332")')

#mycursor.execute("SELECT * FROM blockNO")
#myresult = mycursor.fetchall()
#print(myresult)
#for x in myresult:
#    if(x[0] == "tn38z2332"):
#        print("found block list %s and his is in %s and lat %s and long %s"%(x[0],x[1],x[2],x[3]))
#mycursor.execute("SELECT * FROM findBlock")
#myresult = mycursor.fetchall()
#print(myresult)
#for x in myresult:
#    if x[0].startswith("TN"):
#        print("no outside vichles")
#    else:
#        print("found block list %s and his is in %s and lat %s and long %s"%(x[0],x[1],x[2],x[3]))
mydb.close()
