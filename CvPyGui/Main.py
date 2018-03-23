import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)
import threading
import threadpool 
from CvPyGui import ImageCvQtContainer
from CvPyGui.ui import gui

Ui_MainWindow = gui.Ui_MainWindow

#shot
shotmark1 = 0
shotmark2 = 0

#更新视图
update1 = 0
update2 = 0

#相机编号
capnum1 = 0
capnum2 = 0

#全局视频分辨率
vw = 640
vh = 480

#录像状态
stop = 1

# pool = threadpool.ThreadPool(4) 

p1 = threading.Thread()
p2 = threading.Thread()
p1.setDaemon(True)
p2.setDaemon(True)

class MyApp(QMainWindow, Ui_MainWindow, threading.Thread):

    filter_count = 0

    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()

    def initUI(self):

        self.original1_image = ImageCvQtContainer.Image(
            'camera1', self.original_frame_lbl)
        self.original2_image = ImageCvQtContainer.Image(
            'camera2', self.processed_frame_lbl)
        self.setBackground()
        self.createButtons()

    def initfrom(self):
        global update1
        update1 = 0
        global update2
        update2 = 0
        self.maxcap=0;
        testmax = 10;
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if(cap.isOpened()):
                self.maxcap+=1
            cap.release()
        self.selecamera1.clear()
        self.selecamera2.clear()

        self.selecamera1.addItems([str(i) for i in range(self.maxcap)])
        self.selecamera2.addItems([str(i) for i in range(self.maxcap)])

    def stopfrom(self):
        global update1
        update1 = 0
        global update2
        update2 = 0
        global p1
        global p2


    def loop1(self,text,w=640,h=480):
        cap = cv2.VideoCapture(int(text))
        global capnum1
        capnum1 = int(text)
        cap.set(3,w);
        cap.set(4,h);
        global update1
        update1 = 1
        global shotmark1
        


        while (update1 == 1):
            ret, frame = cap.read() 
            if shotmark1 == 1:
                fn = self.lineEdit.text()
                name = fn + "video1.jpg"
                cv2.imwrite(name, frame)
                shotmark1 = 0
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original1_image.updateImage(frame)
        # cap.release()
        cv_img_rgb = np.zeros((700,700,3))
        self.original1_image.updateImage(cv_img_rgb)

    def selecamera1act(self,text,w=640,h=480):
        global p1
        p1=threading.Thread(target=self.loop1,args=(text,w,h))
        p1.setDaemon(True)
        p1.start()
         # threading.Thread.start_new_thread(loop1,text,w=640,h=480)

    def loop2(self,text,w=640,h=480):
        cap = cv2.VideoCapture(int(text))
        global capnum2
        capnum2 = int(text)
        cap.set(3,w);
        cap.set(4,h);
        global update2
        update2 = 1
        global shotmark2

        while (update2 == 1):
            ret, frame = cap.read() 
            if shotmark2 == 1:
                fn = self.lineEdit.text()
                name = fn + "video2.jpg"
                cv2.imwrite(name, frame)
                shotmark2 = 0
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original2_image.updateImage(frame)
        # cap.release()
        cv_img_rgb = np.zeros((700,700,3))
        self.original2_image.updateImage(cv_img_rgb)

    def selecamera2act(self,text,w=640,h=480):
        global p2
        p2=threading.Thread(target=self.loop2,args=(text,w ,h ))
        p2.setDaemon(True)
        p2.start()

    def threadRe(self,text="",w=640,h=480):
        global stop
        stop = 0
        c = 1
        fn = self.lineEdit.text()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if capnum1 == capnum2:
            c = 0
        cap1 = cv2.VideoCapture(capnum1)
        if c != 0:
            cap2 = cv2.VideoCapture(capnum2)
            name2 = fn + "video2.avi"
            out2 = cv2.VideoWriter(name2,fourcc, 20.0, (640,480))
        name1 = fn + "video1.avi"
        out1 = cv2.VideoWriter(name1,fourcc, 20.0, (640,480))
        
        while(cap1.isOpened()):
                ret1, frame1 = cap1.read()
                out1.write(frame1)
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                self.original1_image.updateImage(frame1)


                if c != 0:
                    ret2, frame2 = cap2.read()
                # # frame = cv2.flip(frame,0)
                    out2.write(frame2)
                    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                    self.original2_image.updateImage(frame2)
                
                if stop == 1:
                        break
        cap1.release()
        out1.release()
        if c != 0:
            cap2.release()
            out2.release()
    def startRe(self):
        global update1
        update1 = 0
        global update2
        update2 = 0
        global p1
        p1=threading.Thread(target=self.threadRe,args=())
        p1.setDaemon(True)
        p1.start()
        

    def endRe(self):
        global stop
        stop = 1
    
    def shotP(self):
        global shotmark1
        shotmark1 = 1
        global shotmark2
        shotmark2 = 1



    def createButtons(self):

        # ComboBox for filter selection
        # self.filter_select.addItems(['Threshold', 'Gaussian Threshold', 'HSV', 'LAB',
        #                              'Erosion', 'Dilation', 'Opening', 'Closing',
        #                              'Top Hat', 'Black Hat', 'Histogram Equalization',
        #                              'Invert', 'Canny', 'Laplacian'])

        # Button for adding filters
        # self.startButton.clicked.connect(self.createNewFilter)
        self.initButton.clicked.connect(self.initfrom)
        self.pushButton.clicked.connect(self.stopfrom)
        self.selecamera1.activated[str].connect(self.selecamera1act)
        self.selecamera2.activated[str].connect(self.selecamera2act)
        self.startButton.clicked.connect(self.startRe)
        self.endButton.clicked.connect(self.endRe)
        self.shotButton.clicked.connect(self.shotP)
        # Checkbox for countours
        # self.countours_check_box.stateChanged.connect(self.calculateOriginal)
        # Button for selecting image
        # self.actionOpen_image.triggered.connect(self.openImage)
        # Buttons for saving images
        # self.actionSave_processed_image.triggered.connect(self.processed_image.saveImage)
        # self.actionSave_original_image.triggered.connect(self.original_image.saveImage)
        # self.actionAbout.clicked.connect(self.about)

    def updateImages(self):
        self.calculateProcessed()
        self.calculateOriginal()

    def setBackground(self):
        cv_img_rgb = np.zeros((700,700,3))
        self.original1_image.updateImage(cv_img_rgb)
        self.original2_image.updateImage(cv_img_rgb)


