import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time



import gspread
from datetime import datetime
sa = gspread.service_account(filename="third-opus-373320-2d83bff7b0f5.json")
sh = sa.open("python crud")

wks = sh.worksheet("Sheet1")
bc='A'
cb='B'
count=0
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
timeout = time.time() + 30*1 #time initializing 
range ="A1:A10" #range initialization
 

path = 'images'
images = []                             #creating the array with name image                ref1(array)
personNames = []                        #creating the array with name personname           ref2(array)
myList = os.listdir(path)               # providing the path of local diratroy             
print(myList)                           #pritin g that hole library
for cu_img in myList:                   #traversing the array with the name cu_image
    current_Img = cv2.imread(f'{path}/{cu_img}')    # created the variable cuurent_img and assigning the content of image directory with the help of loop
    images.append(current_Img)                      # adding current_image data to array of ref1  with the help of loop
    personNames.append(os.path.splitext(cu_img)[0]) # splittig the loop image and storing the name of image into personname ref2

print(personNames)                                  #tatal name stored in personname (ref2) will be displayed


def faceEncodings(images):                                  #just created the function naming as (fun1) for refrence with the parameter of images ref1
    encodeList = []                                         #created the array with the name of encodelist ref3
    for img in images:                                      # with the help of image varible we traversing the hole images(ref1) array
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)          # converting the image into bgr to rgb using cvt color function
        encode = face_recognition.face_encodings(img)[0]    # encoding the image with help of face_recognition function__faceencoding and storing into incode variable 
        encodeList.append(encode)                           # encoded variable is now stored into encodelist ref3

    return encodeList                                       #returning  all the encoded list of images




# def attendance(name):                                       #creating the fun2 for storing the attendence in csv file
    with open('attendence.csv', 'r+') as f:                 #with refrence variable f we are accesing the attendence.csv with read and write mode
        myDataList = f.readlines()                          #reading the hole csv file in the formate in list ,means transformed/splitted into lines as hole list
        nameList = []                                       #creating the name list array ref4
        for line in myDataList:                             #checking th emy data list wih help of variable line
            entry = line.split(',')                         #splitting the above list line into small small sentences wherever there is ',' comma in the line
            nameList.append(entry[0])                       #adding entry data into namelist ref4
        if name not in nameList:                            #name is getting from another function and we checking if it was  there or not in the list
            time_now = datetime.now()                       #creaiting the variable timenow with the help of imported library we are getting the current date and time 
            tStr = time_now.strftime('%H:%M:%S')            # tstr stores the current time
            dStr = time_now.strftime('%d/%m/%Y')            # dstr stores the current date
            f.writelines(f'\n{name},{tStr},{dStr}')         #now we are appending name,date,time into our csv file 
def attendance(name):
    ce=wks.get(range)
    nameList=[]
    for line in ce:
        inside=line[0]
        nameList.append(inside)
    if name not in nameList:
        global count
        count=count+1;
        print(count)
        d=str(count)
        c=bc+d
        e=cb+d
        wks.update(c,name)
        wks.update(e,current_time)


encodeListKnown = faceEncodings(images)                 #new list of known images           ref5
print('All Encodings Complete!!!')

cap = cv2.VideoCapture(0)                          # initilizing the webcam of the computer (0 means internal)(1 meas external)

empty="priod over"
while True:
    if time.time() >= timeout :
        count=count+1;
        h=str(count)
        c=bc+h
        wks.update(c,empty)
        t=1
        if t == 1:
            timeout=time.time()+10 #time increment
            #range increment
            j=str(count)
            k=str(count+10)
            range=(bc+j)+":"+(bc+k)
            t=0

    ret, frame = cap.read()                                     # return two value boolean and actual data(video/photo frame)
    # faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)         #resizing the frame witch is returned by read()
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)              #converting the face image bgrto rgb

    facesCurrentFrame = face_recognition.face_locations(faces)                      #A list of tuples of found face locations in css (top, right, bottom, left) order
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame) #encoding the current detected face with face_locations

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame): 
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  #comparing currentencodedframe with ref5
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  #get a euclidean distance for each comparison face and distance tells you how similar the faces are return array
        # print(faceDis)
        matchIndex = np.argmin(faceDis)      #min element of the array in a particular axis. 

        if matches[matchIndex]:                                      #if ture 
            name = personNames[matchIndex].upper()                   # ref2(array)of person name in name variable in upper case
            print(name)
            y1, x2, y2, x1 = faceLoc                                        # face current frames
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4                 # increasing size by multiplying by 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)        #creating two frames
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED) #creating the frames
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) #putting the name above the face
            attendance(name)                                #givng name as the parameter to atendence function fun2
            

    cv2.imshow("camara", frame)                             #it will displaty that frame into screen 
    if cv2.waitKey(10) == 13:                               #if any key was pressed by the programmer then programm will end 
        break                                               #breaking the while loop

cap.release()                                               #ending the camara  
cv2.destroyAllWindows()                                     #it will distroy all the
