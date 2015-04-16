import pickle
camera_link = []
camera_no = []
number_of_cameras=raw_input("Enter the number of cameras: ")
number_of_cameras=int(number_of_cameras)
for i in xrange(number_of_cameras):
	link = raw_input("Enter camera link for camera no '%d': "%i)
	if i==3:
		camera_link.append("http://admin:cifcharob@"+link+"/video/mjpg.cgi")
	else:
		camera_link.append("http://admin:cif@"+link+"/video/mjpg.cgi")


	camera_no.append(i)

f = open("initialization.txt","w+")
pickle.dump(camera_link,f)