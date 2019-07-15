
# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py


# import the necessary packages
from collections import deque
from imutils.video import FPS
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import cv2
import time
import threading


#center_p = (0,0)
#center_n = (1,1)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

pts = deque(maxlen=args["buffer"])
size = 1
dif = 30
dif2 = 5

pts_r = deque(maxlen=args["buffer"])

pts_b = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = VideoStream(src=0).start()
    fps = FPS().start()
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    fps = FPS().start()

time.sleep(2.0)
fps = FPS().start()

ancho = 320
alto = 240


# keep looping
def tracking_completo():
	while True:
		centro_a = -2
		centro_n = -2
		if args.get("video"):
			(grabbed, frame) = camera.read()
		else:
			frame = camera.read()

	    # if we are viewing a video and we did not grab a frame,
	    # then we have reached the end of the video
		if args.get("video") and not grabbed:
			break

		if frame is None:
			break

	    # grab the frame from the threaded video stream
	    # resize the frame, blur it, and convert it to the HSV
	    # color space

		frame = cv2.resize(frame, (int(ancho), int(alto)))
		frame2 = cv2.resize(frame, (int(ancho), int(alto)))

	    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	    # construct a mask for the color "green", then perform
	    # a series of dilations and erosions to remove any small
	    # blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

	    # find contours in the mask and initialize the current
	    # (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None

	    # only proceed if at least one contour was found
		if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	
		# only proceed if the radius meets a minimum size
			if radius > 10:
			    # draw the circle and centroid on the frame,
			    # then update the list of tracked points
				if (center != None):
					if((center[0] >= ancho/3) & (center[0] <= ancho*2/3) & (center[1] >= alto/3) & (center[1] <= alto*2/3)):
						cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
						cv2.circle(frame, center, 5, (0, 255, 0), -1)
						pts_b.appendleft(center)
						pts_r.clear()
					else:
						cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
						cv2.circle(frame, center, 5, (0, 0, 255), -1)
						pts_r.appendleft(center)
						pts_b.clear()

		    # loop over the set of tracked points
		for i in range(1, len(pts_b)):
			# if either of the tracked points are None, ignore
			# them
			if pts_b[i - 1] is None or pts_b[i] is None:
				continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			if (abs(pts_b[i][0] - pts_b[i-1][0]) < dif or abs(pts_b[i][1] - pts_b[i-1][1]) < dif):
				cv2.line(frame, pts_b[i - 1], pts_b[i], (0, 255, 0), thickness)

		    # loop over the set of tracked points
		for i in range(1, len(pts_r)):
			# if either of the tracked points are None, ignore
			# them
			if pts_r[i - 1] is None or pts_r[i] is None:
				continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			if ((abs(pts_r[i][0] - pts_r[i-1][0]) < dif) or (abs(pts_r[i][1] - pts_r[i-1][1]) < dif)):
				cv2.line(frame, pts_r[i - 1], pts_r[i], (0, 0, 255), thickness)

		    # Centro
		if (center != None):
#			print("Dentro")
			if((center[1] > 0) & (center[1] < alto/3)): #Si esta en los tres cuadrados de arriba
				if((center[0] > 0) & (center[0] < ancho/3)):
					centro_n = 1 #La pelota esta en el cuadro de arriba-izquierda

				elif((center[0] > ancho/3) & (center[0] < ancho*2/3)):
					centro_n = 2 #La pelota esta arriba en medio
				else:
					centro_n = 3 #La pelota esta arriba a la derecha

			elif((center[1]>alto/3) & (center[1]<alto*2/3)): 	#else if centro esta en alguno de los tres cuadrante de arriba -> centro_n = 2
				if((center[0] > 0) & (center[0] < ancho/3)):
					centro_n = 4 #La pelota esta en el cuadro de medio-izquierda

				elif((center[0] > ancho/3) & (center[0] < ancho*2/3)):
					centro_n = 5 #La pelota esta medio en medio
				else:
					centro_n = 6 #La pelota esta medio a la derecha

			elif((center[1]>alto*2/3) & (center[1]<alto)): 	#else if centro esta en alguno de los cuadrantes de abajo -> centro_n = 3
				if((center[0] > 0) & (center[0] < ancho/3)):
					centro_n = 7 #La pelota esta en el cuadro de abajo-izquierda

				elif((center[0] > ancho/3) & (center[0] < ancho*2/3)):
					centro_n = 8 #La pelota esta abajo en medio
				else:
					centro_n = 9 #La pelota esta abajo a la derecha	

			else:
				centro_n = 0 #Si esta dentro de los limites de la camara pero no esta en el centro, centro_n = 0.
		#            print(center[0])
		 #           print(center[1])
		else:    
			centro_n = -1 #Si no se detecta, centro_n = -1
#		print (centro_n)
	    # Grid
		cv2.line(frame2, (0, int(alto/3)), (ancho, int(alto/3)), (255, 0, 0), 2)
		cv2.line(frame2, (0, int(alto*2/3)),
		    (ancho, int(alto*2/3)), (255, 0, 0), 2)

		cv2.line(frame2, (int(ancho/3), 0), (int(ancho/3), alto), (255, 0, 0), 2)
		cv2.line(frame2, (int(ancho*2/3), 0),
		    (int(ancho*2/3), alto), (255, 0, 0), 2)

		    # Transparencia
		alpha = 0.4
		cv2.addWeighted(frame2, alpha, frame, 1-alpha, 0, frame)

		    # update the FPS counter
		fps.update()

		    # show the frame to our screen
		    #cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		    # if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

		    
		if( (centro_n == 1) and (centro_a != centro_n) ): #Cuando se pulsa el joystick, se comprueba si esta en el centro.
	    #    print(centro_n)
			centro_a = centro_n
	  #      f = open("detected.txt", "w") 
	   #     f.write("1") #arriba-izquierda

		elif((centro_n == 2) and (centro_a != centro_n)):
	     #   print(centro_n)
			centro_a = centro_n
	      #  f = open("detected.txt", "w")
	       # f.write("2")#arriba_medio

		elif((centro_n == 3) and (centro_a != centro_n)):
	#        print(centro_n)
			centro_a = centro_n
	 #       f = open("detected.txt", "w")
	  #      f.write("3")#arriba_derecha

		elif( (centro_n == 4) and (centro_a != centro_n) ): #Cuando se pulsa el joystick, se comprueba si esta en el centro.
	   #     print(centro_n)
			centro_a = centro_n
	    #    f = open("detected.txt", "w") 
	     #   f.write("4") #medio_izquierda

		elif((centro_n == 5) and (centro_a != centro_n)):
	      #  print(centro_n)
			centro_a = centro_n
	       # f = open("detected.txt", "w")
	       # f.write("5")#medio_medio

		elif((centro_n == 6) and (centro_a != centro_n)):
	       # print(centro_n)
			centro_a = centro_n
	       # f = open("detected.txt", "w")
	       # f.write("6")#medio_derecha

		elif( (centro_n == 7) and (centro_a != centro_n) ): #Cuando se pulsa el joystick, se comprueba si esta en el centro.
	       # print(centro_n)
			centro_a = centro_n
	       # f = open("detected.txt", "w") 
	       # f.write("7") #abajo_izquierda

		elif((centro_n == 8) and (centro_a != centro_n)):
	       # print(centro_n)
			centro_a = centro_n
	      #  f = open("detected.txt", "w")
	       # f.write("8")#abajo_medio

		elif((centro_n == 9) and (centro_a != centro_n)):
	       # print(centro_n)
			centro_a = centro_n
	       # f = open("detected.txt", "w")
	       # f.write("9")#abajo_derecha

		elif( (centro_n == -1 or centro_n == 0) and (centro_a != centro_n)):
	       # print(centro_n)
			centro_a = centro_n
	       # f = open("detected.txt", "w") 
	       # f.write("-1")
	    
		break

	return centro_n

# stop the timer and display FPS information
fps.stop()
#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()
