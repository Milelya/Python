import tkinter as tk
from tkinter import font  as tkfont
from tkinter import StringVar
from cv2 import *
import numpy as np
from PIL import Image
from PIL import ImageTk
from subprocess import call

font20=("Times",20)
font35=("Times",35)
font40=("Times",40)
lightBlue='#86A6DF'
darkBlue='#5068A9'
photo_name ='test.jpg'  
cmd = 'raspistill -t 5 -o /home/pi/Desktop/vision/' + photo_name
#Problème de rapidité de prise
#upgrade possible:
#prendre un flux vidéo constant et prise de frame sur event -> réduit l'init et gagne environ 300ms par prise
#rapidité théorique: 80 FPS -> 12.5 ms
#					 30 FPS -> 33.3 ms
#overclock processeur -> besoin de meilleur refroidissement processeur
#assigné la frame sur la RAM plutôt que la carte SD -> besoin d'apprendre à le faire et sécurité pour éviter le stack overflow
totalRebut=0
totalCounter=0
i=0

class MainPage():
	def __init__(self):
		#INIT Tkinter frame
		self.win = tk.Tk()
		self.win.title("Vision A.R.")
		self.win.geometry("1280x800")
		self.win.minsize(1280, 800)
		self.win.config(background='#264556')
		#Variable
		global totalRebut
		global nonBlackResult
		global processedFrame
		self.rebutCounter = tk.StringVar()
		self.rebutCounter.set("0 pcs")
		self.rebutPercent = tk.StringVar()
		self.rebutPercent.set("0 %")
		self.totalCounter=0

		homeFrame = tk.Frame(self.win, background='#B2B2B2')
		homeFrame.grid(column=0,row=0)
		homeFrame.columnconfigure(0,minsize=750)
		homeFrame.columnconfigure(1,minsize=530)
		homeFrame.rowconfigure(0,minsize=800)
		#Split homeFrame in two column
		leftFrame = tk.Frame(homeFrame)
		leftFrame.grid(column=0,row=0)
		leftFrame.columnconfigure(0,minsize=600)
		leftFrame.columnconfigure(1,minsize=150)
		leftFrame.rowconfigure(0,minsize=150)
		leftFrame.rowconfigure(1,minsize=650)
		rightFrame = tk.Frame(homeFrame)
		rightFrame.grid(column=1,row=0)
		rightFrame.columnconfigure(0,minsize=530)
		rightFrame.rowconfigure(0,minsize=400)
		rightFrame.rowconfigure(1,minsize=200)
		rightFrame.rowconfigure(2,minsize=200)
		#Fill left column with :
			#rebutFrame
		rebutFrame=tk.Frame(leftFrame,background=lightBlue)
		rebutFrame.grid(column=0,row=0)
		rebutFrame.columnconfigure(0,weight=1,minsize=200)
		rebutFrame.columnconfigure(1,weight=2,minsize=400)
		rebutFrame.rowconfigure(0,minsize=75)
		rebutFrame.rowconfigure(1,minsize=75)
			#Fill rebutFrame with:
				#rebutLabel
		rebutLabel=tk.Label(rebutFrame,text="Rebut: ",background=lightBlue,font=font40,fg="white")
		rebutLabel.grid(column=0,row=0)
				#percentRebut
		percentRebut=tk.Label(rebutFrame,textvariable=self.rebutPercent,background=lightBlue,font=font40,fg="white")
		percentRebut.grid(column=1,row=0)
				#partsRebut
		partsRebut=tk.Label(rebutFrame,textvariable=self.rebutCounter,background=lightBlue,font=font40,fg="white")
		partsRebut.grid(column=1,row=1)
		
			#razFrame
		razFrame=tk.Frame(leftFrame,background='#F30000')
		razFrame.grid(column=1,row=0)
		razFrame.columnconfigure(0,minsize=150)
		razFrame.rowconfigure(0,minsize=75)
		razFrame.rowconfigure(1,minsize=75)
		razFrame.bind('<Button-1>',self.razCompteur)
			#Fill razFrame with:
				#razLabelText1
		razLabelText1=tk.Label(razFrame,text="RAZ",font=font20,fg="white",background='#F30000')
		razLabelText1.grid(column=0,row=0)
				#razLabelText2
		razLabelText2=tk.Label(razFrame,text="Compteur",font=font20,fg="white",background='#F30000')
		razLabelText2.grid(column=0,row=1)
			#cameraFrame
		self.cameraFrame=tk.Frame(leftFrame,background='#3CF267')
		self.cameraFrame.grid(column=0,row=1,columnspan=2)
		self.cameraFrame.rowconfigure(0,minsize=650)
		self.cameraFrame.columnconfigure(0,minsize=750)
		#Convert image to display it
		#initFrame=ImageTk.PhotoImage(file='initFrame.jpg')
		self.cameraDisplayLabel=tk.Label(self.cameraFrame)
		self.cameraDisplayLabel.grid(column=0,row=0)
		self.imageProcessing()
		
		#Fill right column with:
			#typeRebutFrame
		typeRebutFrame=tk.Frame(rightFrame,background='white')
		typeRebutFrame.grid(column=0,row=0)
		typeRebutFrame.columnconfigure(0,minsize=530)
		typeRebutFrame.rowconfigure(0,minsize=100)
		typeRebutFrame.rowconfigure(1,minsize=100)
		typeRebutFrame.rowconfigure(2,minsize=100)
		typeRebutFrame.rowconfigure(3,minsize=100)
			#Fill typeRebutFrame with:
				#typeRebutText
		typeRebutText=tk.Label(typeRebutFrame,text="Type de rebut",font=font40,background='white',fg=darkBlue)
		typeRebutText.grid(column=0,row=0)
				#firstTypeRebut
		firstTypeRebut=tk.Label(typeRebutFrame,text="Manque de joint (1.5%)",font=font20,background=darkBlue,fg='white')
		firstTypeRebut.grid(column=0,row=1,ipadx=100,sticky="E")
				#secondTypeRebut
		secondTypeRebut=tk.Label(typeRebutFrame,text="Manque de joint (1.5%)",font=font20,background=darkBlue,fg='white')
		secondTypeRebut.grid(column=0,row=2,ipadx=60,sticky="E")
				#thirdTypeRebut
		thirdTypeRebut=tk.Label(typeRebutFrame,text="Manque de joint (1.5%)",font=font20,background=darkBlue,fg='white')
		thirdTypeRebut.grid(column=0,row=3,ipadx=30,sticky="E")
			#Split right column in two for 1 row
		splittedRightColumnFrame=tk.Frame(rightFrame)
		splittedRightColumnFrame.grid(column=0,row=1)
		splittedRightColumnFrame.columnconfigure(0,minsize=330)
		splittedRightColumnFrame.columnconfigure(1,minsize=200)
		splittedRightColumnFrame.rowconfigure(0,minsize=200)
			#firstSide
		firstSide=tk.Frame(splittedRightColumnFrame,background='#F56200')
		firstSide.grid(column=0,row=0)
		firstSide.columnconfigure(0,minsize=330)
		firstSide.rowconfigure(0,minsize=100)
		firstSide.rowconfigure(1,minsize=100)
				#Fill firstSide with:
					#apprentissageCouleurLine1
		apprentissageCouleurLine1=tk.Label(firstSide,text="Apprentissage",background='#F56200',fg='white',font=font35)
		apprentissageCouleurLine1.grid(column=0,row=0)
					#apprentissageCouleurLine2
		apprentissageCouleurLine2=tk.Label(firstSide,text="couleur",background='#F56200',fg='white',font=font35)
		apprentissageCouleurLine2.grid(column=0,row=1)
			 #secondSide
		secondSide=tk.Frame(splittedRightColumnFrame,background=darkBlue)
		secondSide.grid(column=1,row=0)
		secondSide.columnconfigure(0,minsize=200)
		secondSide.rowconfigure(0,minsize=200)
				#Fill secondSide with:
					#loginButton
		loginButton=tk.Label(secondSide,text="Login",background=darkBlue,fg='white',font=font35)
		loginButton.grid(column=0,row=0)
			
			#displayChoiceFrame
		displayChoiceFrame=tk.Frame(rightFrame,background=lightBlue)
		displayChoiceFrame.grid(column=0,row=2)
		displayChoiceFrame.columnconfigure(0,minsize=530)
		displayChoiceFrame.rowconfigure(0,minsize=80)
		displayChoiceFrame.rowconfigure(1,minsize=60)
		displayChoiceFrame.rowconfigure(2,minsize=60)
				#Fill displayChoice with:
					#labelDisplayChoice
		labelDisplayChoice=tk.Label(displayChoiceFrame,text="Choix de l'affichage",background=lightBlue,fg='white',font=font20)
		labelDisplayChoice.grid(column=0,row=0)
					#choice1DisplayChoice
		choice1DisplayChoice=tk.Label(displayChoiceFrame,text="Dernière pièce",background='white',fg=darkBlue,font=font20)
		choice1DisplayChoice.grid(column=0,row=1)
					#choice2DisplayChoice
		choice2DisplayChoice=tk.Label(displayChoiceFrame,text="Dernière pièce mauvaise",background=darkBlue,fg='white',font=font20)
		choice2DisplayChoice.grid(column=0,row=2)




		#Pack the global frame
		homeFrame.pack(expand=True,fill="both")
		self.win.mainloop()

	def imageProcessing(self):
		global nonBlackResult
		global processedFrame
		global totalRebut
		global totalCounter
		global i
		nonBlackResult=0
		threshMin=0
		threshMax=255
		edgeThreshMin=0
		edgeThreshMax=40
		hueMin=0
		hueMax=255
		saturationMin=150
		saturationMax=255
		valueMin=0
		valueMax=255
		hsvMin= np.array([hueMin,saturationMin,valueMin])
		hsvMax= np.array([hueMax,saturationMax,valueMax])
		scale=0.22
		self.takeFrame()
		totalCounter+=1
		if i%2:
			frame=cv2.imread("image2.jpg",1)
		else:
			frame=cv2.imread("image2.jpg",1)
		i+=1
		height, width, _ = frame.shape
		frame=cv2.resize(frame,(int(width*scale),int(height*scale)))
		#Convert frame to hsv
		hsvMask=cv2.inRange(frame,hsvMin,hsvMax)
		grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayImg=cv2.bitwise_and(grayImg,grayImg,mask=hsvMask)
		_,grayMask=cv2.threshold(grayImg,thresh=threshMin,maxval=threshMax,type=cv2.THRESH_BINARY)
		grayFiltered= cv2.bitwise_and(grayImg,grayMask)
		grayImgForEdges=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(grayImgForEdges,edgeThreshMin,edgeThreshMax*2)
		cercle = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1.2, 250)
		if cercle is not None:
			cercle = np.round(cercle[0, :]).astype("int")
			for (x, y, r) in cercle:
				compteur=cv2.circle(grayFiltered, (x, y), r-18, (0, 0, 0), 4)
				nonZero=cv2.countNonZero(compteur)
				compteur2=cv2.circle(grayFiltered,(x, y), r-26, (0, 0, 0), 2)
				nonZero2=cv2.countNonZero(compteur2)
				nonBlackResult=nonZero-nonZero2
				print(nonZero)
				print(nonZero2)
				print(nonBlackResult)
				cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
				cv2.circle(frame, (x, y), r-18, (0, 0, 255), 2)
				cv2.circle(frame,(x, y), r-26, (0, 0, 255), 2)
		else:
				nonBlackResult=999
		processedFrame=cv2.resize(frame,(int(width*scale),int(height*scale)))
		cameraImg=Image.fromarray(processedFrame)
		lastImg=ImageTk.PhotoImage(cameraImg)
		self.cameraDisplayLabel.configure(image=lastImg)
		self.cameraDisplayLabel.image=lastImg
		if nonBlackResult > 10:
				totalRebut+=1
				self.cameraFrame["background"]="red"
				self.rebutCounter.set(str(totalRebut)+' pcs')
				self.rebutPercent.set(str(round(totalRebut*100/totalCounter,2))+' %')
		else:
				self.cameraFrame["background"]='#3CF267'
				self.rebutPercent.set(str(round(totalRebut*100/totalCounter,2))+' %')
		self.win.after(200,self.imageProcessing)

	def takeFrame(self):
		call([cmd], shell=True)
		print(totalRebut)

	def razCompteur(self,event):
		global totalCounter
		global totalRebut
		totalCounter=0
		totalRebut=0
		self.rebutCounter.set(str(totalRebut)+' pcs')
		self.rebutPercent.set(str(round(totalRebut*100/totalCounter,2))+' %')

UL=MainPage()