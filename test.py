import cv2
import numpy as np
import argparse
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
img = cv2.imread(args["image"],0)
cimg = cv2.imread(args["image"])


def Area(radius):
    return radius**2*np.pi


AREA_EURO_mm = (23.25/(2*np.pi))**2*np.pi

#cimg = cv2.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)


circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=100)

circles = np.uint16(np.around(circles))
for j,i in enumerate(circles[0,:]):
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    #print(i[2],img.shape[0])
    area = (Area(radius=i[2])/img.size)*300
    #print(area)
cv2.imshow('detected circles',img)
cv2.waitKey(0)

#cv2.destroyAllWindows()


green = [130, 158, 0]

# You define an interval that covers the values
# in the tuple and are below and above them by 20
diff = 10

# Be aware that opencv loads image in BGR format,
# that's why the color values have been adjusted here:

lower = (0, 0, 0)
upper =(0, 255,255) 
# Scale your BIG image into a small one:


# Calculate the new dimensions
width = int(img.shape[1] )
height = int(img.shape[0])

# Resize the image:

# check out the image resized:
cv2.imshow("img resized", img)
cv2.waitKey(0)
# for riga,i in enumerate(img):
#     for j in range(0,len(riga),3):
#         if riga[j]


#image_copy = np.copy(img)
lower_blue = np.array([200,0,0]) 
upper_blue = np.array([250,250,255])
mask = cv2.inRange(cimg,lower_blue,upper_blue)

# Check out the binary mask:
cv2.imshow("binary mask", mask)
cv2.waitKey(0)

# Now, you AND the mask and the input image
# All the pixels that are white in the mask will
# survive the AND operation, all the black pixels
# will remain black
output = cv2.bitwise_and(img, img, mask=mask)

# Check out the ANDed mask:
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

# Print the color percent, use 2 figures past the decimal point
print('green pixel percentage:', np.round(colorPercent, 2))

# numpy's hstack is used to stack two images horizontally,
# so you see the various images generated in one figure:
cv2.imshow("images", np.hstack([img, output]))
cv2.waitKey(0)