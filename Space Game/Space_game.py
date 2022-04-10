import numpy as np
import cv2 
import glob
from pupil_apriltags import Detector
import pyautogui
import os
import pygame, random, sys, os
from pygame.locals import *
import time 










def get_corner_point():

    
    good_images = 0
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("img")
    img_counter=0
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('opencv_frame_*.jpeg')
    run = True 
    while run:
            ret, frame = cam.read()
            if not ret:
                print(Fore.RED+"failed to grab frame") 
                break
        
            img_name = "open_cv_{}.jpeg".format(img_counter)
            img_counter+=1
            cv2.imwrite(img_name, frame)
            print("__________________________________________________________________________________________________")
            print('Reading frame')
            print("__________________________________________________________________________________________________")
            img = cv2.imread(img_name)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            ret_1, corners = cv2.findChessboardCorners(gray, (7,6), None)
            if ret_1 == True and good_images<14:
                good_images+=1
                print("###############################################################################################")
                print('Found a frame for calibration , {} more to go'.format(14-good_images))
                print ("Displaying calibration output..............")
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (7,6), corners2, ret_1)
                cv2.imshow('img', img)
                cv2.waitKey(5000)
                
                print("###############################################################################################")
            try:
                os.remove(img_name)
            except:
                continue
                
            if good_images>=14:
                try:
                    f= open('camera_matrix.txt','w')
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
                    print("{} , {} , {} , {}".format(mtx[0][0] , mtx[1][1] , mtx[0][2] , mtx[1][2]), file = f)
                    print("Camera calibration completed succesfully")
                    f.close()
                except:
                    pass
                run = False
            
            
    cv2.destroyAllWindows()




            



########################SPACE GAME###############


pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WINDOWHEIGHT = 750
WINDOWWIDTH = 750

FONT = pygame.font.SysFont(None, 48)
SPACE = pygame.image.load( 'bg.png')
SPACE = pygame.transform.scale(SPACE, (750, 750))
SPACE2 = pygame.image.load( 'gameoverbg.png')
SPACE2 = pygame.transform.scale(SPACE2, (WINDOWWIDTH, WINDOWHEIGHT))

bg_img = pygame.image.load('mainbg.png')
bg_img = pygame.transform.scale(bg_img, (WINDOWWIDTH, WINDOWHEIGHT))


def terminate():
    pygame.quit()
    sys.exit()

def Menu(fx,fy,cx,cy):
    timer = 0
    color = BLUE
    switch = False
    mouse_x = WINDOWWIDTH
    mouse_y = WINDOWHEIGHT

   
    tickCounter = 0
    enemies = []
    amountOfEnemies = 0
    score = 0
    FPS = 75
    hitShots = 0
    totalShots = 0
 
    CIRCLERADIUS = 150
    f_x = fx
    f_y = fy
    c_x  = cx
    c_y =  cy
    cam = cv2.VideoCapture(0)
    press_count_0=0
    press_count_1=0
    press_count_2=0
    
    

    img_counter=0
    at_detector = Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,

                           refine_edges=1,
                           decode_sharpening=0.25,
                           debug=0)
    while True:
        gameDisplay.blit(SPACE, (0,0))
        difficultyRects = []
        difficultyRects.append(pygame.Rect(5, 450, 240, 100))
        difficultyRects.append(pygame.Rect(255, 450, 240, 100))
        difficultyRects.append(pygame.Rect(505, 450, 240, 100))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        ret, frame = cam.read()
        if not ret:
                print("failed to grab frame")
                break
        
        img_name = "april_tag{}.jpeg".format(img_counter)
        img_counter+=1
        cv2.imwrite(img_name, frame)
        
        img = cv2.imread(img_name)
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        cv2.waitKey(2)#changed to 2 from 5
        try:
            tags = at_detector.detect( gray, estimate_tag_pose=True, camera_params=[f_x,f_y,c_x,c_y], tag_size=0.015)
            mouse_x = (640-tags[0].center[0])*1.172
            mouse_y = (tags[0].center[1])*1.5625
            if mouse_x>WINDOWWIDTH:
                mouse_x =WINDOWWIDTH
            if mouse_y>WINDOWHEIGHT:
                mouse_y=WINDOWHEIGHT
        except:
            pass
        mouseX = mouse_x
        mouseY = mouse_y
        
                
       
        try: 
                os.remove(img_name)
        except:
                continue
        cv2.destroyAllWindows()                
                    
                    
                    
                    
                    
        if mouseX and mouseY:
               

               
               if difficultyRects[0].collidepoint(mouseX,mouseY) and difficultyRects[1].collidepoint(mouseX,mouseY) == False and difficultyRects[2].collidepoint(mouseX,mouseY) == False  :
                        press_count_0+=1
                        press_count_2=0
                        press_count_1=0
                        
                        
               if difficultyRects[1].collidepoint(mouseX,mouseY) and difficultyRects[0].collidepoint(mouseX,mouseY) == False and difficultyRects[2].collidepoint(mouseX,mouseY) == False  :
                        
                        press_count_1+=1
                        press_count_0=0
                        press_count_2=0
               if difficultyRects[2].collidepoint(mouseX,mouseY) and difficultyRects[1].collidepoint(mouseX,mouseY) == False and difficultyRects[0].collidepoint(mouseX,mouseY) == False  :
                        
                        press_count_2+=1
                        press_count_0=0
                        press_count_1=0
               if difficultyRects[0].collidepoint(mouseX,mouseY) == False and difficultyRects[1].collidepoint(mouseX,mouseY) == False and difficultyRects[2].collidepoint(mouseX,mouseY) == False  :
                        press_count_0=0
                        press_count_1=0
                        press_count_2=0

               
                    
                    
               if press_count_0 == 50:
                     
                     game("easy",fx,fy,cx,cy)
               if press_count_1 == 50:
                     
                     game("medium",fx,fy,cx,cy)
               if press_count_2 == 50:
                     
                     game("hard",fx,fy,cx,cy)

               
               
                     
                     
                     
               
            
              
                

        

                            
        for rect in difficultyRects:
            pygame.draw.rect(windowSurface, RED, rect)
        drawText("Pick a difficulty", windowSurface, 90, 150, pygame.font.SysFont(None, 112), color)
        drawText("Easy", windowSurface, 83, 485, FONT , BLACK)
        drawText("Medium", windowSurface, 312, 485,FONT , BLACK)
        drawText("Hard", windowSurface, 580, 485,FONT , BLACK)
        mainClock.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = BLUE
        elif timer % 50 == 0:
            color = RED

        pygame.draw.line(windowSurface, BLACK, (mouseX, mouseY + 15),
                        (mouseX, mouseY - 15), 2)
        pygame.draw.line(windowSurface, BLACK, (mouseX + 15, mouseY),
                        (mouseX - 15, mouseY), 2)
        pygame.draw.rect(windowSurface, BLUE, (mouseX -20, mouseY +20,
                        press_count_0,20))
        pygame.draw.rect(windowSurface, BLUE, (mouseX-20 , mouseY +20,
                        press_count_1,20))
        pygame.draw.rect(windowSurface, BLUE, (mouseX-20 , mouseY +20,
                        press_count_2,20))
        pygame.display.update()

def drawText(text, surface, x, y, font = FONT, color = RED):
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObject, textRect)

def gameOver(totalShots, hitShots, difficulty, score,fx,fy,cx,cy):
    pygame.mouse.set_visible(True)
    i=0
    if totalShots != 0 and hitShots != 0:
        accuracy = round(hitShots/totalShots * 100)
    else:
        accuracy = 0
    gameDisplay.blit(SPACE2, (0,0))
    drawText("GAME OVER", windowSurface, 200, 325, pygame.font.SysFont(None, 72, True))
    drawText("Taking You To Menu Screen", windowSurface, 120, 380)
    
    drawText("Score: " + str(score), windowSurface, 308, 450)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                windowSurface.fill(BLACK)
                Menu(fx,fy,cx,cy)
            if event.type == KEYDOWN:
                terminate()
        if i == 500000:
                windowSurface.fill(BLACK)
                Menu(fx,fy,cx,cy)
        i+=1
    


def populateConfig(difficulty):
    global targetImage
    targetImage = pygame.image.load("ufo-removebg.png")
    config = {}
    if(difficulty == "easy"):
        difficultyFile = open("easy.txt", "r")
    elif(difficulty == "medium"):
        difficultyFile = open("medium.txt", "r")
    elif(difficulty == "hard"):
        difficultyFile = open("hard.txt", "r")
    for line in difficultyFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    targetImage = pygame.transform.scale(targetImage, (config["enemySize"],config["enemySize"]))
    difficultyFile.close()
    return config



def game(difficulty,fx,fy,cx,cy):
    config = populateConfig(difficulty)
    i=0
    
    pygame.mouse.set_visible(False)
    
    mouse_x = WINDOWWIDTH /2
    mouse_y = WINDOWHEIGHT /2

   
    tickCounter = 0
    enemies = []
    amountOfEnemies = 0
    score = 0
    FPS = 75
    hitShots = 0
    totalShots = 0
    STARTINGTIME = config.get("time")
    CIRCLERADIUS = 150
    f_x = fx
    f_y = fy
    c_x  = cx
    c_y =  cy
    cam = cv2.VideoCapture(0)
    
    

    img_counter=0
    at_detector = Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,

                           refine_edges=1,
                           decode_sharpening=0.25,
                           debug=0)
    while True:
        if(config.get("time") <= 0):
            gameOver(totalShots, hitShots, difficulty, score ,fx,fy,cx,cy)
        tickCounter += 1
        if(tickCounter % FPS == 0):
            config["time"] -= 1
        gameDisplay.fill((0,0,0))
        gameDisplay.blit(bg_img,(i,0))
        gameDisplay.blit(bg_img,(WINDOWWIDTH+i,0))
        
        if i == (WINDOWWIDTH):
            i = 0
        i -= 1

        if (amountOfEnemies == 0):
            config["time"] = STARTINGTIME
            while(amountOfEnemies != config.get("maxAmountOfEnemies")):
                enemies.append(pygame.Rect((random.randint(0,WINDOWWIDTH - config.get("enemySize"))),
                                           (random.randint(0,WINDOWHEIGHT - config.get("enemySize"))),
                                           config.get("enemySize"), config.get("enemySize")))
                if enemies[amountOfEnemies].topleft[0] < 135 and enemies[amountOfEnemies].topleft[1] < 65:
                    enemies.pop(amountOfEnemies)
                else:
                    amountOfEnemies += 1

        ret, frame = cam.read()
        if not ret:
                print("failed to grab frame")
                break
        
        img_name = "april_tag{}.jpeg".format(img_counter)
        img_counter+=1
        cv2.imwrite(img_name, frame)
        
        img = cv2.imread(img_name)
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        cv2.waitKey(2)#changed to 2 from 5
        try:
            tags = at_detector.detect( gray, estimate_tag_pose=True, camera_params=[f_x,f_y,c_x,c_y], tag_size=0.015)
            mouse_x = (640-tags[0].center[0])*1.172
            mouse_y = (tags[0].center[1])*1.5625
            if mouse_x>WINDOWWIDTH:
                mouse_x =WINDOWWIDTH
            if mouse_y>WINDOWHEIGHT:
                mouse_y=WINDOWHEIGHT
        except:
            pass
        mouseX = mouse_x
        mouseY = mouse_y
        
                
       
        try: 
                os.remove(img_name)
        except:
                continue
        cv2.destroyAllWindows()

        for enemy in enemies[:]:
                    print(enemy.topleft)
                    print(enemy.topright)
                    print(mouseX)
                    print(mouseY)
                    print('___')
                    if mouseX > (enemy.topleft[0]+50) and mouseX < (enemy.bottomright[0]-50)\
                       and mouseY > (enemy.topleft[1]+25) and mouseY < (enemy.bottomright[1]-40):
                        pygame.mixer.Channel(1).play(hitSound)
                        enemies.remove(enemy)
                        amountOfEnemies -= 1
                        score += 1
                        hitShots += 1


        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            
                
                
                
            if event.type == MOUSEBUTTONDOWN:
                pygame.mixer.Channel(0).play(shootSound)
                totalShots += 1
                for enemy in enemies[:]:
                    if mouseX > enemy.topleft[0] and mouseX < enemy.bottomright[0]\
                       and mouseY > enemy.topleft[1] and mouseY < enemy.bottomright[1]:
                        pygame.mixer.Channel(1).play(hitSound)
                        enemies.remove(enemy)
                        amountOfEnemies -= 1
                        score += 1
                        hitShots += 1
                
                        
                                           
        
        for enemy in enemies:
            windowSurface.blit(targetImage, enemy)
        
        pygame.draw.line(windowSurface, WHITE, (mouseX, mouseY + 15),
                        (mouseX, mouseY - 15), 2)
        pygame.draw.line(windowSurface, WHITE, (mouseX + 15, mouseY),
                        (mouseX - 15, mouseY), 2)
        drawText("Time: " + str(config.get("time")), windowSurface, 8,8)
        drawText("Score: " + str(score), windowSurface, 8,38)
        pygame.display.update()
        mainClock.tick(FPS)




#main_control of our program
camera_matrix_choice  = input('Do you want to perform a new calibration (y/n): ').lower()
run = True
while run:
    if camera_matrix_choice == 'y':
        get_corner_point()
        f= open('camera_matrix.txt','r')
        
        
    elif camera_matrix_choice == 'n':
        try:
            f= open('camera_matrix.txt','r')
        except:
            
            print('No camera calibration found on local computer!')
            print('Entering camera calibration mode....................................')
            get_corner_point()
            f= open('camera_matrix.txt','r')
            
        
    s  = f.read().strip('\n').split(',')
    fx,fy,cx,cy = float(s[0]),float(s[1]),float(s[2]),float(s[3])
    f.close()
        

        


        
    gameDisplay = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("SHOOT")

    shootSound = pygame.mixer.Sound("snipersound.wav")
    hitSound = pygame.mixer.Sound("metalHit.wav")
    shootSound.set_volume(0.07)
    hitSound.set_volume(0.07)


    enemies = []
    Menu(fx,fy,cx,cy)
            
    run = False
            
            
            
        



            
