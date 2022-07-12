import cv2
import numpy as np

def findbeam(savedimage):
	#read image replace with camera image later
	image = cv2.imread(savedimage)
	gray_img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	img2 = cv2.GaussianBlur(gray_img, (3,3), 0)
	img = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#	img = cv2.medianBlur(gray_img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
 	#fitting parameters
	minDist=50
	dp = 1
	param1 = 1
	param2 = 7
	minRadius = 1
	maxRadius = 90
	#find circles
	circles	= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp = dp,minDist = minDist,param1=param1,param2=param2,minRadius=minRadius ,maxRadius=maxRadius)
	a, b,r = 0,0,0
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for pt in circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]
			cv2.circle(image, (a, b), r, (0, 255, 0), 2)
#			cv2.circle(cimg, (a, b), r, (0, 255, 0), 2)	
	else:
		print('No Circles Found') 
	reala = int((a+1)/2 - 92.5)
	realb = int(92.5 - (b+1)/2)
	#Find image center
	ax= gray_img.shape[0]
	ay= gray_img.shape[1]
#	print(a,b, 'found place')
#	print(ax,ay, 'gray_img shape')
	realr=r/2
#	print(reala,realb,realr)
	diff = np.asarray([reala, realb, realr])

	#Display Image
#	cv2.imshow("HoughCirlces", image)
#	cv2.imshow("blkwhite", cimg)
#	cv2.waitKey()
#	cv2.destroyAllWindows()
	#Return Result
	result = diff
#	result = np.append(circles[0][0],[ax,ay,realr], axis=0)
	return result
bx, by, ax, ay, x, y,r = 0, 0,0,0,0,0,0

#x, y, r = findbeam('1.png')
#print([x,y])
#print(r)
#print(ax)
#print(ay)
