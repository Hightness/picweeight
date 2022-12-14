import cv2
import numpy as np
import argparse,os



#area of various coins in mm
coin_areas={"1 euro":(23.25/(2*np.pi))**2*np.pi}




def main(args):
    img = cv2.imread(args["image"],0)
    cimg = cv2.imread(args["image"])
    coin_area=detect_circles(img)
    if not coin_area:return
    upper = np.array([90,90,255]) 
    lower = np.array([0,0,40])
    green_perc=detect_color(lower,upper,cimg)
    volume = beta_volume_prop(coin_area,green_perc,"1 euro")
    print('\n'*20+f"detected area:{volume}"+'\n'*8)

def beta_volume_prop(coin_area,green_perc,coin_type):
    stimated_height=12#mm
    volume = (green_perc*coin_areas[coin_type])*coin_area*stimated_height
    return volume


def circle_area(radius):
    return radius**2*np.pi

def detect_circles(img):
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=100)
    circles = np.uint16(np.around(circles))[0,:]
    if len(circles)==1:
        print("too many coins in image")
        for i in circles:
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        cv2.imshow('detected circles',img)
        cv2.waitKey(0)
        return 0

    else:
        coin=circles[0]
        # draw the outer circle
        cv2.circle(img,(coin[0],coin[1]),coin[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(coin[0],coin[1]),2,(0,0,255),3)
        return (circle_area(radius=coin[2])/img.size)*300
        #cv2.imshow('detected circles',img)
        #cv2.waitKey(0)

def detect_color(lower,upper,img):

    cv2.imshow("image", img)
    cv2.waitKey(0)
    #image_copy = np.copy(img)
    mask = cv2.inRange(img,lower,upper)

    # Check out the binary mask:
    #cv2.imshow("binary mask", mask)
    #cv2.waitKey(0)

    # Now, you AND the mask and the input image
    # All the pixels that are white in the mask will
    # survive the AND operation, all the black pixels
    # will remain black
    output = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("ANDed mask", output)
    cv2.waitKey(0)

    # You can use the mask to count the number of white pixels.
    # Remember that the white pixels in the mask are those that
    # fall in your defined range, that is, every white pixel corresponds
    # to a green pixel. Divide by the image size and you got the
    # percentage of green pixels in the original image:
    ratio_green = cv2.countNonZero(mask)/(img.size/3)

    # This is the color percent calculation, considering the resize I did earlier.
    colorPercent = (ratio_green * 100)
    return colorPercent

    # numpy's hstack is used to stack two images horizontally,
    # so you see the various images generated in one figure:
    #cv2.imshow("images", np.hstack([img, output]))
    #cv2.waitKey(0)

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help = "path to the image")
    args = vars(ap.parse_args())
    main(args)