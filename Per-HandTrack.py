import array
import cv2
import time
from matplotlib import pyplot as plt
import HandTrackModule as htm
import math
import csv
import cvzone
import pandas as pd

z=0
answer=array.array('i',(0 for i in range (-33,33)))
pathCsv="sorular.csv"
path2Csv="sonuçlar.csv"
with open(pathCsv,newline='\n') as f:
    reader=csv.reader(f)
    dataAll=list(reader)[1:]
with open(path2Csv,newline='\n') as g:
    reader=csv.reader(g)
    dataSonuc=list(reader)[1:]
#print(dataAll)
#print(dataAll[0])
qNo=0
i=0
wCam, hCam = 1200,800
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

def answer0():
    circle1 = cv2.circle(img, (170, 550), 40, (169, 169, 169), 6)
    circle2 = cv2.circle(img, (370, 550), 40, (169, 169, 169), 6)
    circle3 = cv2.circle(img, (570, 550), 40, (169, 169, 169), 6)
    circle4 = cv2.circle(img, (770, 550), 40, (169, 169, 169), 6)
    circle5 = cv2.circle(img, (970, 550), 40, (169, 169, 169), 6)
    circle11 = cv2.circle(img, (170, 550), 37, (0, 0, 255), cv2.FILLED)
    circle22 = cv2.circle(img, (370, 550), 37, (0, 0, 255), cv2.FILLED)
    circle33 = cv2.circle(img, (570, 550), 37, (0, 0, 255), cv2.FILLED)
    circle44 = cv2.circle(img, (770, 550), 37, (0, 0, 255), cv2.FILLED)
    circle55 = cv2.circle(img, (970, 550), 37, (0, 0, 255), cv2.FILLED)

detector = htm.handDetector(detectionCon=0.7,maxHands=1)
while True:
    succes, img = cap.read()
    img=cv2.flip(img, 1)
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img, draw=False)
    if qNo<18:
        if len(lmList) !=0 and qNo==0:
            xa, ya = lmList[4][1], lmList[4][2]
            xb, yb = lmList[8][1], lmList[8][2]
            lengtho = math.hypot(xa - xb, ya - yb)
            img, bboxa = cvzone.putTextRect(img, str(dataAll[qNo]), [135, 100], 1.5, colorT=(255, 255, 255),colorR=(173, 112, 68),
                                                                offset=50, border=5, colorB=(214, 157, 247))
            img, bboxb = cvzone.putTextRect(img,"START", [1080, 560], 1.75, colorT=(255, 255, 255),
                                           colorR=(199, 178, 145),
                                           offset=50, border=10, colorB=(191, 191, 191))

            if lengtho <90 and xb<1160 and yb<560 and xb>1080 and yb>520:
                    i+=1
                    qNo+=1
        if i == 17:
            col_list=["X","Y","C"]
            df = pd.read_csv(path2Csv, usecols=col_list)
            xUser = answer[1]+ answer[2]+ answer[3]+ answer[4]+ (answer[5]+ answer[6]+ answer[7]+ answer[8])*-1
            yUser = answer[9] + answer[10]+ answer[11]+ answer[12]+ answer[13]+answer[14]+answer[15]+ answer[16]
            eu1=df["X"]
            eu2=df["Y"]
            color=df["C"]
            euclidean=[0]*len(dataSonuc)
            for z in range(len(dataSonuc)):
               euclidean[z]=math.sqrt((xUser-eu1[z])**2+(yUser-eu2[z])**2)
            min_value=min(euclidean)
            min_index=euclidean.index(min_value)
            print("En yakın komşu:","(",eu1[min_index],eu2[min_index],")")
            print("En yakın komşuya uzaklık:", min_value)
            if color[min_index]=='gray':
                print("Your Personality is: Intellect - Extraversion")
            if color[min_index]=='blue':
                print("Your Personality is: Imagination-Extraversion")
            if color[min_index]=='purple':
                print("Your Personality is: Intellect-Surgency")
            if color[min_index]=='brown':
                print("Your Personality is: Imagination-Surgency")
            #print("                     %", abs((yUser / 16) * 100), "  - %", abs((xUser / 16) * 100))
            for i in range(len(dataSonuc)):
                plt.scatter(eu1[i],eu2[i],c=color[i])
            plt.scatter(xUser, yUser, c="red")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("Personality Test")
            plt.show()
            header = [answer[1] + answer[2] + answer[3] + answer[4] + (answer[5] + answer[6] + answer[7] + answer[8])*-1,
                      answer[9] + answer[10]+ answer[11]+ answer[12] + answer[13] + answer[14] + answer[15] + answer[16],color[min_index]]
            c = open('sonuçlar.csv', 'a', newline='\n')
            writer = csv.writer(c)
            writer.writerow(header)
            c.close()
            i=0
            qNo=0
        if qNo>0:
            img, bbox = cvzone.putTextRect(img, str(dataAll[qNo]), [100, 100], 2, colorT=(255, 255, 255), colorR=(173, 112, 68),
                                                   offset=50, border=5, colorB=(214, 157, 247))
            cv2.rectangle(img,(1050,200),(1140,250),(0, 0, 0), cv2.FILLED)
            cv2.putText(img, "BACK", (1060, 230), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(img, "Strongly Disagree", (65,485), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(img, "Disagree", (323,485), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(img, "Neutral", (520,485), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(img, "Agree", (732,485), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(img, "Strongly Agree", (875, 485), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2)

            answer0()

            if len(lmList) != 0:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1+x2) // 2, (y1+y2) // 2
                length = math.hypot(x2-x1,y2-y1)
                        #print(length)
                if length < 35 and x2 < 1150 and y2 < 260 and x2 > 1040 and y2 > 190:
                    i-=1
                    qNo-=1
                    time.sleep(0.3)
                if length<35 and x2<210 and y2<590 and x2>130 and y2>510:
                    circle11=cv2.circle(img, (170, 550), 37, (0,255,0), cv2.FILLED)
                    answer[qNo] = -2
                    qNo+=1
                    i+=1
                    time.sleep(0.3)
                if length<35 and x2<410 and y2<590 and x2>330 and y2>510:
                    circle22=cv2.circle(img, (370, 550), 37, (0,255,0), cv2.FILLED)
                    answer[qNo] = -1
                    qNo+=1
                    i+=1
                    time.sleep(0.3)
                if length<35 and x2<610 and y2<590 and x2>530 and y2>510:
                    circle33=cv2.circle(img, (570, 550), 37, (0,255,0), cv2.FILLED)
                    #print("yea")
                    answer[qNo] = 0
                    qNo+=1
                    i+=1
                    time.sleep(0.3)
                if length<35 and x2<810 and y2<590 and x2>730 and y2>510:
                    circle44=cv2.circle(img, (770, 550), 37, (0,255,0), cv2.FILLED)
                    #print("yea")
                    answer[qNo] = 1
                    qNo+=1
                    i+=1
                    time.sleep(0.3)
                if length<35 and x2<1010 and y2<590 and x2>930 and y2>510:
                    circle55=cv2.circle(img, (970, 550), 37, (0,255,0), cv2.FILLED)
                    #print("yea")
                    answer[qNo] = 2
                    qNo+=1
                    i+=1
                    time.sleep(0.3)

    cv2.imshow("Berk", img)
    cv2.waitKey(1)



