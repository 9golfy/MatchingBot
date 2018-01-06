import pyautogui as pg
import random
import time
import cv2
import numpy as np
import os
d = {}
tmpdict ={}

def automateClick():
    pg.click(397,712)
    file = open("boardposition.txt")
    for line in file:
        l = line.split()
        d[l[0]] = l[1:]
    t = 35
    file.close()
    while t > 0 :
        time.sleep(0.5)
        r = random.randint(0, len(d)-1)
        k = list(d)[r]
        x = int(d[list(d)[r]][0])
        y = int(d[list(d)[r]][1])
        pg.click(x,y)
        t -= 1
        screenShot(x,y,k)

def screenShot(x,y,k):
    time.sleep(0.5)
    sc = pg.screenshot(region=(x,y,37,34))
    sc.save("sc/tmp.png")
    imageProcessing(x,y,k)


def imageProcessing(x,y,k):
    time.sleep(0.5)
    filename = "sc/tmp.png"
    img1 = cv2.imread(filename)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    pathPNG = os.chdir("E:\\CodeLearning\\Python\\BotDev\\MatchingBot\\png")
    l = []
    i = 0
    for f in os.listdir(pathPNG):
        i+=1
        img2 = cv2.imread(f)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img1_gray, img2_gray, cv2.TM_CCOEFF_NORMED)
        res = np.float(res)
        l.append(tuple([int(i),float(res)]))

    maxScore = sorted(l, key=lambda x: x[1], reverse = True)[0]
    os.chdir("E:\\CodeLearning\\Python\\BotDev\\MatchingBot")
    global tmpdict
    tmpdict[k] = [x,y,maxScore[0]]
    storeAnswer(k,tmpdict[k][2])

def storeAnswer(k1,v1):
        try:
            for k2, v2 in list(tmpdict.items()):
                if (k1 != k2 and v1 == v2[2]):
                    pg.click(tmpdict[k2][0],tmpdict[k2][1])
                    pg.click(tmpdict[k1][0],tmpdict[k1][1])
                    print("{} {}, It's Matched, Click".format(v1,v2[2]))
                    tmpdict.pop(k1), tmpdict.pop(k2)
                    d.pop(k1), d.pop(k2)
                    break
                elif(k1 == k2 and v1 == v2[2]):
                    print("...")
                else:
                    print("{} {}, Not Matched".format(v1,v2[2]))
        except:
            pass

automateClick()
