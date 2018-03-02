import glob
import os
import cv2
import numpy as np

if __name__ =="__main__":
    print("Coin count!")

    #Path setup
    image_raw_path="/home/mhuertas/Work/RoboND/Project2/raw/"
    image_reduced_path="/home/mhuertas/Work/RoboND/Project2/reduced/"

    #Read the images
    image_names = glob.glob(image_raw_path+'*.jpeg')
    for ipx_img, image_name in enumerate(image_names):
  
        #Read image
        img = cv2.imread(image_name)
        img = cv2.resize(img,
                             (0,0), fx=0.25, fy=0.25,
                             interpolation = cv2.INTER_AREA)
        img_blur = cv2.medianBlur(img,5)
        img_gray = cv2.cvtColor(img_blur,cv2.COLOR_RGB2GRAY)
        
        #Detect circles (coins)
        circles = cv2.HoughCircles(img_gray,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=100)
    
        #If not the three coins detected ignore image    
        if circles is None  or np.size(circles)!= 9:
            print(image_name," Rejected")
            continue
        
        #Sort the circles
        circles = np.uint16(np.around(circles[0])) 
        circles  = np.sort(circles.view('uint16,uint16,uint16'),order=['f0'],axis=0).view(np.uint16)
    
        for i in circles:
            # draw the outer circle
            cv2.circle(img_gray,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img_gray,(i[0],i[1]),2,(0,0,255),3)
         
        # Loop every circle of the image    
        for ipx,circle in enumerate(circles):
            #Create a mask with the circle area
            mask = np.zeros((270,480,3), np.uint8)
            cv2.circle(mask,(circle[0],circle[1]),circle[2],(1,1,1),-1)

            #Mask the image    
            img_masked = img*mask

            #Include the image masked into a image of 256x256
            img_coin = np.zeros((256, 256,3))
            img_coin[128-circle[2]:128+circle[2],
                     128-circle[2]:128+circle[2],:] = img_masked[circle[1]-circle[2]:circle[1]+circle[2],
                                                          circle[0]-circle[2]:circle[0]+circle[2],:]
            
            #Build the image name, depending on the class
            coin_class = ""         
            if ipx == 0:
                coin_class="coin20"
            elif ipx == 1:
                coin_class="coin100"
            elif ipx == 2:
                coin_class="coin10"
            
            image_coin_name = image_reduced_path + coin_class + "/" + image_name.split("/")[-1].split('.')[0]+"_"+str(ipx)+".jpg"
            
            #Save the image.
            cv2.imwrite(image_coin_name ,img_coin)
            
        #if ipx_img == 2:
        #    break      
        
        #cv2.imshow('detected circles',img_gray)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        