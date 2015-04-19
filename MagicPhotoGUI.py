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
		toolBar = Frame(self)
		toolBar.pack(side=TOP, fill=X)
		openButton = Button(toolBar, text=u'open', command = self.on_open)
		openButton.pack(side=LEFT, expand=NO)
		saveButton = Button(toolBar, text=u'save', command = self.on_save)
		saveButton.pack(side=LEFT, expand=NO)
		magicButton = Button(toolBar, text=u'magic', command = self.on_magic)
		magicButton.pack(side=LEFT, expand=NO)
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
			self.imgForShow = Image.open("1.gif")
		self.imgForLable = ImageTk.PhotoImage(self.imgForShow)
		self.imgLabel.config(image=self.imgForLable)
		self.lock.release()		
		if self.magicing == True:
			threading.Timer(0.02, self.next_frame).start()
	def on_magic(self):
		if self.magicing == False:
			self.magicing = True
			self.imgForShow = Image.open("1.gif")
			self.imgForLable = ImageTk.PhotoImage(self.imgForShow)
			self.imgLabel.config(image=self.imgForLable)
			threading.Timer(0.02, self.next_frame).start()
			thread.start_new_thread(self.on_magic_thread, ())
	def on_magic_thread(self):
		tile_size = 48
		if self.img:
			if self.tiles[tile_size] == None:
				self.tiles[tile_size], temp = MagicPhoto.load_tile("tile/" + str(tile_size) + "/*")
			new_size = (self.img.size[0]/tile_size*tile_size, self.img.size[1]/tile_size*tile_size)
			self.img = self.img.resize(new_size)
			self.img = MagicPhoto.make_output(self.tiles[tile_size], self.img)
			self.magicing = False
			self.make_show()
if __name__ == "__main__":
	MagicFrame().mainloop()
