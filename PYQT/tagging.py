#!/usr/bin/env python
#coding: utf-8

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

import names as Pixeler

from FloorPlan import braille_transfer
from FloorPlan import split_cubeV2 as split_cube
from FloorPlan import excute_blender

class SizeLabel (QtWidgets.QLabel):

	def setValue(self, value):

		self.setText(str(value))


class Tagging (QtWidgets.QDockWidget):

	def __init__(self, title, context, signals, Parent=None):

		super(Tagging, self).__init__(title, Parent)

		self.context = context
		self.signals = signals
		self.parent = Parent
		self.setAllowedAreas(Qt.RightDockWidgetArea)
		self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

		# Llista de widgets (configuració de cada eina del programa)
		self.widgets = self.createWidgets()
		self.signals.updateTool.connect(self.updateWidget)

		self.updateWidget()

	def createWidgets(self):

		# Creem una llista amb tots el widgets i la retornem
		l = []

		l.append(self.createtaggingWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())
		l.append(QtWidgets.QWidget())

		return l

	def createSelectionWidget(self):

		w = QtWidgets.QWidget()
		w.setObjectName("Tagging")
		w.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
		vbox = QtWidgets.QVBoxLayout()

		transparent = QtWidgets.QCheckBox(self.context.getText("tool_properties_selection", "transparent"), self)
		transparent.setChecked(self.context.transparentSelection)
		transparent.toggled.connect(self.context.setTransparentSelection)

		vbox.setAlignment(QtCore.Qt.AlignTop)
		vbox.addWidget(transparent)
		w.setLayout(vbox)

		return w

	def createtaggingWidget(self):
		w = QtWidgets.QWidget()
		grid = QtWidgets.QGridLayout()
		self.titleEdit = QtWidgets.QLineEdit("input here")
		self.addButton = QtWidgets.QPushButton("add")
		self.okButton = QtWidgets.QPushButton("OK")
		self.saveButton = QtWidgets.QPushButton("Transfer 3D model")
		self.lbl1 = QtWidgets.QLabel('plz input')
		self.lbl2 = QtWidgets.QLabel('')
		grid.addWidget(self.titleEdit, 1, 1)
		grid.addWidget(self.okButton, 1, 3)
		grid.addWidget(self.addButton, 1, 2)
		grid.addWidget(self.saveButton, 1,4)
		grid.addWidget(self.lbl1, 2, 1)
		grid.addWidget(self.lbl2, 3, 1)
		self.addButton.clicked.connect(self.addclick)
		self.okButton.clicked.connect(self.Okclick)
		self.saveButton.clicked.connect(self.saveclick)
		w.setLayout(grid)

		return w

	def addclick(self):
		#print(self.titleEdit.text())
		#print(self.context.currentTool)
		#print(self.context.custom_X,self.context.custom_Y)
		print("x1,y1,x2,y2 : {},{},{},{}".format(str(self.context.custom_selection_X1),str(self.context.custom_selection_Y1),str(self.context.custom_selection_X2),str(self.context.custom_selection_Y2)))
		
		if len(self.context.taglist) >= 8:
			self.lbl1.setText("The tag is already full. (You can have up to 8 tags)")
		# real size 6.1*9.3 -> minimun size 16 * 22
		elif (self.context.custom_selection_X2-self.context.custom_selection_X1) >= 22 and (self.context.custom_selection_Y2-self.context.custom_selection_Y1) >=16:
			self.context.custom_X = self.context.custom_selection_X1+((self.context.custom_selection_X2-self.context.custom_selection_X1)//2)
			self.context.custom_Y = self.context.custom_selection_Y1+((self.context.custom_selection_Y2-self.context.custom_selection_Y1)//2)
			self.context.custom_X -= 4.7
			self.context.custom_Y -= 3.1
			
			self.lbl1.setText(" x : "+str(int(self.context.custom_X))+" y : "+str(int(self.context.custom_Y))+" text : "+self.titleEdit.text())
			self.context.taglist.append([str(int(self.context.custom_X)),str(int(self.context.custom_Y)),self.titleEdit.text()])

		else:
			self.lbl1.setText("select box is too small, plz minimum x,y : 22 x 16")

		self.titleEdit.setText("input here")
		'''
		color picker
		self.lbl1.setText(" x : "+str(int(self.context.custom_X))+" y : "+str(int(self.context.custom_Y))+" text : "+self.titleEdit.text())
		self.context.taglist.append([str(int(self.context.custom_X)),str(int(self.context.custom_Y)),self.titleEdit.text()])
		self.titleEdit.setText("input here")
		'''
	def saveclick(self):
		self.lbl1.setText("Start save Process")
		self.context.currentImage().fileName = "temp.jpg"
		self.context.currentImage().save()

		self.SC = split_cube.main()
		print("successful : Split cube")
		for i in range(len(self.context.current_taglist)):
			self.tag = self.context.current_taglist[i]
			# [ x, y, number, place_name ]
			self.context.braille_transfer_taglist.append([self.tag[0],self.tag[1],braille_transfer.number_transfer(i),braille_transfer.main(self.tag[2])])
		print("successful : braille transfer")

		make_model_res = excute_blender.excute(self.SC,self.context.braille_transfer_taglist,braille_transfer.main(self.context.titlename))
		if make_model_res: self.lbl1.setText("successful make 3D model")
		else: self.lbl1.setText("failed make 3D model")

		self.context.current_taglist = list()
		self.context.braille_transfer_taglist = list()
		self.context.titlename = ""

	def Okclick(self):
		if self.context.titlename == "":
			self.titleEdit.setText("plz input Title!")
			print(self.context.taglist)
			self.lbl1.setText("tagging 완료! 총 :"+str(len(self.context.taglist))+"개 태그를 추가하셨습니다.")
			self.lbl2.setText(str(self.context.taglist))
			self.context.current_taglist = self.context.taglist
			self.context.taglist = list()
			self.context.titlename = "wait"
		else:
			self.context.titlename = self.titleEdit.text()
			self.titleEdit.setText("END")
			print(self.context.titlename)
			self.lbl1.setText("tagging 완료! 총 :"+str(len(self.context.current_taglist))+"개 태그를 추가하셨습니다.")
			self.lbl2.setText("Title 설정 완료! 건물 : "+self.context.titlename)


	def createPencilWidget(self):

		w = QtWidgets.QWidget()
		w.setObjectName("Tagging")
		w.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
		vbox = QtWidgets.QVBoxLayout()

		hbox1 = QtWidgets.QHBoxLayout()

		pencilSizeLabel = QtWidgets.QLabel(self.context.getText("tool_properties_pencil", "size"))
		slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
		slider.setValue(self.context.pencilSize)
		self.pencilSize = SizeLabel(str(self.context.pencilSize))

		slider.setMaximum(9)
		slider.setMinimum(1)
		slider.setPageStep(1)
		slider.setValue(self.context.pencilSize)
		slider.valueChanged.connect(self.context.setPencilSize)
		slider.valueChanged.connect(self.pencilSize.setValue)
		self.signals.updatePencilSize.connect(slider.setValue)

		hbox1.addWidget(pencilSizeLabel)
		hbox1.addWidget(slider)
		hbox1.addWidget(self.pencilSize)

		"""
		hbox2 = QtWidgets.QHBoxLayout()
		hbox2.addWidget(QtWidgets.QLabel("Alpha:"))
		alpha = QtWidgets.QSpinBox()
		alpha.setMinimum(0)
		alpha.setMaximum(255)
		alpha.setValue(255)
		alpha.valueChanged.connect(self.setPencilAlpha)
		alpha.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
		hbox2.addWidget(alpha)
		"""
		hbox2 = QtWidgets.QHBoxLayout()
		eraser = QtWidgets.QCheckBox(self.context.getText("tool_properties_pencil", "eraser"), self)
		eraser.setChecked(self.context.secondaryColorEraser)
		eraser.toggled.connect(self.toggleSecondaryColorEraser)
		hbox2.addWidget(eraser)

		vbox.setAlignment(QtCore.Qt.AlignTop)

		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		w.setLayout(vbox)

		return w

	def setPencilSize(self, size):

		self.pencilSize.setText(str(size))
		self.context.pencilSize = size

	def setPencilAlpha(self, alpha):

		self.context.pencilAlpha = alpha

	def toggleSecondaryColorEraser(self):

		self.context.secondaryColorEraser = not self.context.secondaryColorEraser

	def createEraserWidget(self):

		w = QtWidgets.QWidget()
		w.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
		vbox = QtWidgets.QVBoxLayout()

		hbox = QtWidgets.QHBoxLayout()

		eraserSizeLabel = QtWidgets.QLabel(self.context.getText("tool_properties_eraser", "size"))
		slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
		slider.setValue(self.context.eraserSize)
		self.eraserSize = SizeLabel(str(self.context.eraserSize))

		slider.setMaximum(9)
		slider.setMinimum(1)
		slider.setPageStep(1)
		slider.setValue(self.context.eraserSize)
		slider.valueChanged.connect(self.context.setEraserSize)
		slider.valueChanged.connect(self.eraserSize.setValue)
		self.signals.updateEraserSize.connect(slider.setValue)

		hbox.addWidget(eraserSizeLabel)
		hbox.addWidget(slider)
		hbox.addWidget(self.eraserSize)

		vbox.setAlignment(QtCore.Qt.AlignTop)

		vbox.addLayout(hbox)
		w.setLayout(vbox)

		return w

	def setEraserSize(self, size):

		self.eraserSize.setText(str(size))
		self.context.eraserSize = size

	def createGradientWidget(self):

		self.v = QtWidgets.QVBoxLayout()

		v2 = QtWidgets.QVBoxLayout()

		self.btn1 = QtWidgets.QRadioButton(self.context.getText("tool_properties_gradient", "horizontal"))
		self.btn2 = QtWidgets.QRadioButton(self.context.getText("tool_properties_gradient", "vertical"))
		self.btn1.setChecked(True)

		self.btn1.clicked.connect( lambda : self.changeDegDir('H') )
		self.btn2.clicked.connect( lambda : self.changeDegDir('V') )

		h = QtWidgets.QHBoxLayout()

		self.label = QtWidgets.QLabel("Transparencia:", self)

		self.AlphaSpin = QtWidgets.QSpinBox(self) 
		self.AlphaSpin.setMinimum(0)
		self.AlphaSpin.setMaximum(255)
		self.AlphaSpin.setValue(255)
		self.AlphaSpin.valueChanged.connect(self.setAlphaValue)

		h.addWidget(self.label)
		h.addWidget(self.AlphaSpin)
		tmp = QtWidgets.QWidget()
		tmp.setLayout(h) 

		self.check = QtWidgets.QCheckBox("Color a Transparente")
		self.check.stateChanged.connect(self.changeDegState)

		v2.addWidget(self.btn1)
		v2.addWidget(self.btn2)
		tmp2 = QtWidgets.QWidget()
		tmp2.setLayout(v2) 

		self.v.addWidget(tmp2) 
		#self.v.addWidget(tmp)
		#self.v.addWidget(self.check)

		w = QtWidgets.QWidget()
		w.setLayout(self.v)
		self.v.addStretch()

		return w


	def changeDegDir(self, state):
		if self.btn1.isChecked():
			self.context.DegDir = 'H'
		elif self.btn2.isChecked():
			self.context.DegDir = 'V'

	def changeDegState(self):
		if self.check.isChecked():
			self.context.DegState = 1
		else:
			self.context.DegState = 2

	def setAlphaValue(self):
		self.context.DegAlpha = self.AlphaSpin.value()
		print(self.context.DegAlpha)

	def updateWidget(self):
		self.setWidget(self.widgets[self.context.currentTool])
