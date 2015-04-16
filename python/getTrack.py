import sys,sqlite3

person = raw_input("Enter Name:  ")
conn2 = sqlite3.connect('Watchmen.db')
cur2 = conn2.execute("SELECT * from PEOPLE WHERE NAME=:name",{"name":str(person)})
rows = cur2.fetchall()
if(rows==None):
  print "Sorry! Person not in database."
else:
  print str(person)+" seen at :"
  for row in rows:
    print str(row[3])+" on "+str(row[2])