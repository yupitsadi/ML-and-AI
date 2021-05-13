import cv2, time, pandas                                    #cv2 used convert pixel into array, pandas store time frame   
from datetime import datetime                               #it is used to record date and time

first_frame=None                                            #used to store first frame    
status_list=[None,None]                                     #it is used to store data, in which time object is enter and exits
times=[]                                                    #to store time 
df=pandas.DataFrame(columns=["Start","End"])                #pandas framework to store data in csv file

#here we start capturing data from camera, in-built camera-0(def) for extenal 1,2 and so on.   cap dshow is used fot direct use data from camera
video=cv2.VideoCapture(0, cv2.CAP_DSHOW)

#loop for capture frames
while True:
    check, frame = video.read()                              #check tell the stauts is 0 or 1 and frame record the data
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)              #it is used to convert capture fram into black and white frames
    gray=cv2.GaussianBlur(gray,(21,21),0)                    #it is used to convert capture fram into bullery frames (which will come handy)

    #this loop is used to find the diffrence
    if first_frame is None:
        first_frame=gray                                     #it is take first framw if there are none
        continue
    #this snippet is used to fid movement/diffrence b/w frames
    delta_frame=cv2.absdiff(first_frame,gray)                                                       #a function which helps in finding the absolute difference between the pixels of the two image arrays
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]                          #it convert pixel B&W according to give input and compaires
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)                                       #it dilate the img so process would become faster 

    #this is snippet will neglect pixel by piexl comparison and action will takes place in required area
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)       

    #loop fo size of pixel and multiple rectangle
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x, y, w, h)=cv2.boundingRect(contour)              #for creating rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)                                      #size of rectangle and color 


    #this snippet is used to record the time frame in which object enters and leaves
    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    #these all display gray, delta frame, thresh frame and detection colored frame respectively
    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)

    #this will hold the displayed frame while refreshing it
    key=cv2.waitKey(1)
    if key==ord('q'):                                   #when Q is pressed it will closed all the activites
        if status==1:
            times.append(datetime.now())                #when q is pressed it will record the last frame
        break

print(status_list)                                      
print(times)

#this snippet will take all the time of object enters and exit the frame this store then in csv file
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

#loction of file
df.to_csv("F:/projects c,c++,python/python/motion dection/Times.csv")

#following code will stop camera and destory all the windows
video.release()
cv2.destroyAllWindows