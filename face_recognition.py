from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x720+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(
                self.root,
                text="Face Recognition",
                font=("Times new roman", 28, "bold"),
                bg="white",
                fg="darkblue",
            )
        title_lbl.place(x=0, y=0, width=1200, height=40)

        # Image
        img_top=Image.open(r"assets\face_detector1.jpg")
        img_top=img_top.resize((550, 700), Image.ADAPTIVE)
        self.photoimg_top=ImageTk. PhotoImage(img_top)

        f_lbl=Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0,y=40,width=550,height=700)

        # Image
        img_bottom=Image.open(r"assets\mobileScreen_FR.jpg")
        img_bottom=img_bottom. resize((650, 700), Image.ADAPTIVE)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

        f_lbl=Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=550, y=40,width=650,height=700)

        # Button
        b1_1 = Button(
            f_lbl,
            text="Face Recognition",
            font=("Times new roman", 16, "bold"),
            command=self.face_recog,
            bg="white",
            fg="darkblue",
            cursor="hand2",
        )
        b1_1.place(x=220, y=620, width=200, height=40)


    # =============== Face Recognition ===============
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
            
            coord = []

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict = clf.predict(gray_image[y:y+h,x:x+w])
                confidence = int((100*(1-predict/300)))

                conn = mysql.connector.connect(
                        host="your_host_name",
                        username="your_mysql_username",
                        password="your_password",
                        database="your_database_name",
                        )
                my_cursor = conn.cursor()

                my_cursor.execute("select name from student where student_id = " + str(id))
                n = my_cursor.fetchone()
                n="+".join(n)

                my_cursor.execute("select course from student where student_id = " + str(id))
                r = my_cursor.fetchone()
                r="+".join(r)

                my_cursor.execute("select Dep from student where student_id = " + str(id))
                d = my_cursor.fetchone()
                d="+".join(d)

                if confidence > 77:
                    cv2.putText(img,f"{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(55, 158, 0),3)
                    cv2.putText(img,f"{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(55, 158, 0),3)
                    cv2.putText(img,f"{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(55, 158, 0),3)
                
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(158, 8, 0),3)

                coord = [x,y,w,h]
            return coord
        
        def recognize(img,clf,faceCascade):
            coord=draw_boundary(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
            return img
        
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer.create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret,img = video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face recognition", img)

            if cv2.waitKey(1) == 13:
                break
        video_cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
