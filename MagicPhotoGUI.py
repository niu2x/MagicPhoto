#-*- coding:utf-8 -*-
from tkinter import *
from tkFileDialog import askopenfilename 
from tkFileDialog import asksaveasfilename 
from PIL import Image, ImageTk
from src import MagicPhoto
class MagicFrame(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)	
		toolBar = Frame(self)
		toolBar.pack(side=TOP, fill=X)
		openButton = Button(toolBar, text=u'open', command = self.on_open)
		openButton.pack(side=LEFT, expand=NO)
		saveButton = Button(toolBar, text=u'save', command = self.on_save)
		saveButton.pack(side=LEFT, expand=NO)
		self.body = Frame(self, width=10, height=10)
		self.body.pack(side=TOP, expand=YES, fill=BOTH)
		self.imgLabel=Label(self.body)
		self.imgLabel.pack(expand=YES, fill=BOTH)
		stateBar = Frame(self)
		stateBar.pack(side=BOTTOM, fill=X)
		Label(stateBar, text="author:niu2x").pack(side=RIGHT)
		self.img = None
	def on_open(self):
		filename = askopenfilename(filetypes=[("JPG", "*.jpg"),("JPEG", "*.jpeg"),("Bitmap", "*.bmp"),("PNG", "*.png")])
		if filename:
			self.img = MagicPhoto.safe_load_img(filename)
			self.imgLabel.config(image=ImageTk.PhotoImage(self.img))
	def on_save(self):
		pass
if __name__ == "__main__":
	MagicFrame().mainloop()
