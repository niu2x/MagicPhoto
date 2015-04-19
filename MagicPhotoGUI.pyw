#-*- coding:utf-8 -*-
from Tkinter import *
from tkFileDialog import askopenfilename 
from tkFileDialog import asksaveasfilename 
from PIL import Image, ImageTk
from src import MagicPhoto
import thread
import threading
class MagicFrame(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.master.title("MagicPhoto")
		toolBar = Frame(self)
		toolBar.pack(side=TOP, fill=X)
		openButton = Button(toolBar, text=u'打开', command = self.on_open)
		openButton.pack(side=LEFT, expand=NO)
		saveButton = Button(toolBar, text=u'保存', command = self.on_save)
		saveButton.pack(side=LEFT, expand=NO)
		magicButton = Button(toolBar, text=u'Magic', command = self.on_magic)
		magicButton.pack(side=LEFT, expand=NO)
		self.tileSizeFrame = Frame(toolBar)
		self.tileSizeFrame.pack(side=LEFT, expand=NO)
		self.tileSizeVar = IntVar()
		self.tileSizeVar.set(48)
		Label(self.tileSizeFrame, text=u"小方块的大小").pack(side=LEFT)
		Radiobutton(self.tileSizeFrame,variable = self.tileSizeVar,text = '32',value = 32).pack(side=LEFT)
		Radiobutton(self.tileSizeFrame,variable = self.tileSizeVar,text = '48',value = 48).pack(side=LEFT)
		Radiobutton(self.tileSizeFrame,variable = self.tileSizeVar,text = '64',value = 64).pack(side=LEFT)
		self.body = Frame(self, width=10, height=10)
		self.body.pack(side=TOP, expand=YES, fill=BOTH)
		self.imgLabel=Label(self.body)
		self.imgLabel.pack(expand=YES, fill=BOTH)
		stateBar = Frame(self)
		stateBar.pack(side=BOTTOM, fill=X)
		Label(stateBar, text="author:niu2x").pack(side=RIGHT)
		self.img = None
		self.imgForShow = None
		self.magicing = False
		self.lock = thread.allocate_lock()
		self.tiles = {48:None, 32:None, 64:None}
		self.busyGif = "media/gif/1.gif"
	def make_show(self):
		self.lock.acquire()
		self.imgForShow = self.img.copy()
		if self.imgForShow.size[0] > 800 or self.imgForShow.size[1] > 500:
			xxx = self.imgForShow.size[0] / 800
			yyy = self.imgForShow.size[1] / 500
			k = max([xxx, yyy])
			self.imgForShow = self.imgForShow.resize((self.imgForShow.size[0]/k, self.imgForShow.size[1]/k))
		self.imgForLable = ImageTk.PhotoImage(self.imgForShow)
		self.imgLabel.config(image=self.imgForLable)
		self.lock.release()
	def on_open(self):
		filename = askopenfilename(filetypes=[("JPG", "*.jpg"),("JPEG", "*.jpeg"),("Bitmap", "*.bmp"),("PNG", "*.png")])
		if filename:
			self.img = MagicPhoto.safe_load_img(filename)
			self.make_show()
	def on_save(self):
		filename = asksaveasfilename(filetypes=[("JPG", "*.jpg"),("JPEG", "*.jpeg"),("Bitmap", "*.bmp"),("PNG", "*.png")])
		if filename:
			try:
				self.img.save(filename)
			except IOError, e:
				showerror(title=u"提示", message=u"保存失败")
	def next_frame(self):
		if self.magicing == False:
			return
		self.lock.acquire()
		try:
			self.imgForShow.seek(self.imgForShow.tell()+1)
		except EOFError, e:
			self.imgForShow = Image.open(self.busyGif)
		self.imgForLable = ImageTk.PhotoImage(self.imgForShow)
		self.imgLabel.config(image=self.imgForLable)
		self.lock.release()		
		if self.magicing == True:
			threading.Timer(0.04, self.next_frame).start()
	def on_magic(self):
		if self.img and self.magicing == False:
			self.magicing = True
			self.imgForShow = Image.open(self.busyGif)
			self.imgForLable = ImageTk.PhotoImage(self.imgForShow)
			self.imgLabel.config(image=self.imgForLable)
			threading.Timer(0.04, self.next_frame).start()
			thread.start_new_thread(self.on_magic_thread, ())
	def on_magic_thread(self):
		tileSize = self.tileSizeVar.get()
		if self.img:
			if self.tiles[tileSize] == None:
				self.tiles[tileSize], temp = MagicPhoto.load_tile("tile/" + str(tileSize) + "/*")
			newSize = (self.img.size[0]/tileSize*tileSize, self.img.size[1]/tileSize*tileSize)
			self.img = self.img.resize(newSize)
			self.img = MagicPhoto.make_output(self.tiles[tileSize], self.img)
			self.magicing = False
			self.make_show()
if __name__ == "__main__":
	MagicFrame().mainloop()
