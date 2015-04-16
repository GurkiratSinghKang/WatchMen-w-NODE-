import sys,sqlite3

person = raw_input("Enter Name:  ")
conn = sqlite3.connect('Watchmen.db')
cur2 = conn.execute("SELECT Max(ID) FROM PEOPLE WHERE NAME='%s';"%(str(person)));
max_id = cur2.fetchone()[0]
if(max_id != None):
  cur2 = conn.execute("SELECT LAST_SEEN_TIME, CAMERA_NO from PEOPLE WHERE NAME=:name and ID=:id",{"name":str(person),"id":int(max_id)})
  need = cur2.fetchone()
  last_known_time = need[0]
  print str(person)+" Last seen on "+str(need[0])+" on  "+str(need[1])
else:
  print "Sorry! Person not in database."