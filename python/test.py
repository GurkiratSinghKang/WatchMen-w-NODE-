import cv2,sys,random,os,math,select,time
import numpy as np
import threading
import sqlite3,datetime,sys
import pickle

f = open("initialization.txt","r")
camera_link = pickle.load(f)
print camera_link
def prompt() :
 sys.stdout.write('\rWatchMen>>  ')
 sys.stdout.flush()



fn_dir='faces'
images = []
lables = []
names = {}
colours={}
id=0
im_width=0
im_height=0
model=None
def getNames():
    global fn_dir,images,lables,names,colours,id

    for subdir in os.listdir(fn_dir):
        if subdir[0]=='.':
            continue
        names[id]=subdir
        colours[id]=(random.randrange(256),random.randrange(256),random.randrange(256))
        subjectpath=os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            if filename[0]=='.':
                continue
            path=os.path.join(subjectpath, filename)
            lable=id
            images.append(cv2.imread(path,0))
            lables.append(int(lable))
        id+=1
        print colours
        print names


def getData():
    global im_width,im_height,model
    im_width=images[0].shape[0]
    im_height=images[0].shape[1]
    model = cv2.createLBPHFaceRecognizer()
    model.load("training_data.xml")

def createTable():
    conn = sqlite3.connect('Watchmen.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS People
             (ID INTEGER  PRIMARY KEY    NOT NULL,
             NAME           TEXT    NOT NULL,
             CAMERA_NO            TEXT     NOT NULL,
             LAST_SEEN_TIME          TEXT    NULL );""")
    conn.close()



def save_person(person_id,person_name,camera,camera_no):
    pos = str(datetime.datetime.now()).find('.')
    time_now=datetime.datetime.strptime(str(datetime.datetime.now())[:pos] , '%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('Watchmen.db')
    #cur2 = conn.execute("SELECT * from PEOPLE WHERE NAME=:name",{"name":str(person_name)})
    cur2 = conn.execute("SELECT Max(ID) FROM PEOPLE WHERE NAME='%s';"%(str(person_name)));
    max_id = cur2.fetchone()[0]
    if(max_id != None):
      cur2 = conn.execute("SELECT LAST_SEEN_TIME, CAMERA_NO from PEOPLE WHERE NAME=:name and ID=:id",{"name":str(person_name),"id":int(max_id)})
      need = cur2.fetchone()
      last_known_time = need[0]

      last_known = datetime.datetime.strptime(last_known_time , '%Y-%m-%d %H:%M:%S')
      threshold = 5.0
      diff = time_now - last_known
      time_diff_tuple = divmod(diff.total_seconds(), 60)
      time_diff=time_diff_tuple[0]
      if ((time_diff)>threshold):
        conn.execute("INSERT INTO PEOPLE (NAME,CAMERA_NO,LAST_SEEN_TIME) VALUES (?,?,?)",(str(person_name),str(camera_no),str(time_now)));
        conn.commit()
      else:
        if(str(need[1])==str(camera_no)):
          cursor = conn.execute("SELECT Max(ID) FROM PEOPLE WHERE NAME='%s';"%(str(person_name)));
          max_id = cursor.fetchone()[0]
          conn.execute("UPDATE PEOPLE SET LAST_SEEN_TIME=? WHERE id=?", (time_now, int(max_id)))
          conn.commit()
        else:
          conn.execute("INSERT INTO PEOPLE (NAME,CAMERA_NO,LAST_SEEN_TIME) VALUES (?,?,?)",(str(person_name),str(camera_no),str(time_now)));
          conn.commit()
    else:
      conn.execute("INSERT INTO PEOPLE (NAME,CAMERA_NO,LAST_SEEN_TIME) VALUES (?,?,?)",(str(person_name),str(camera_no),str(time_now)));
      conn.commit()

    conn.close()






faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")



def main():
    getNames()
    getData()
    createTable()
    cameras=[]


    for i in xrange(len(camera_link)):
        cameras.append(cv2.VideoCapture(camera_link[i]))

    while True:
        frames=[]
        for i in xrange(len(camera_link)):
            frames.append(cameras[i].read())
            gray = cv2.cvtColor(frames[i][1], cv2.COLOR_BGR2GRAY)
            #print frames[i]
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            place = ""
            if i==0:
              place = "Robotics Lab Right Cam"
            elif i==1:
              place = "Robotics Lab Left Cam"
            elif i==2:
              place = "Schneider Lab Cam"
            elif i==3:
              place = "Robotics Lab Center Cam"

        # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resize=cv2.resize(face,(im_width, im_height))
                prediction=model.predict(face_resize)
                print prediction

                cv2.rectangle(frames[i][1], (x,y), (x+w, y+h), colours[prediction[0]], 3)
                if(prediction[1]>50):
                    cv2.putText(frames[i][1], '%s %.0f'%(names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, colours[prediction[0]])
                    save_person(prediction[0],names[prediction[0]],camera_link[i],place)

      
                else:
                    cv2.putText(frames[i][1], '%s'%(""), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, colours[prediction[0]])


        both1 = np.hstack((frames[0][1],frames[1][1]))
        both2=np.hstack((frames[2][1],frames[3][1]))
        four = np.vstack((both1,both2))
        small = cv2.resize(four, (0,0), fx=0.5, fy=0.5)
        # Display the resulting frame
        cv2.imshow('Video', small)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    for i in xrange(len(camera_link)):
        cameras[i].release()
    cv2.destroyAllWindows()

main()

