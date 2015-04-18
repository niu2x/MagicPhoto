# -*- coding:utf-8 -*-
import argparse
from HTMLParser import HTMLParser
from HTMLParser import HTMLParseError
from urlparse import urljoin
import urllib
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class PictureGraber(HTMLParser):
	def __init__(self, startURL, maxNumber):
		HTMLParser.__init__(self)
		self.maxNumber = maxNumber
		self.picturePaths = set()
		self.nextURLs = [startURL]
		self.visited = set()
		self.currentURL = None
		self.flag = 0
		self.body = False
	def handle_starttag(self, tag, attrs):
		if "body" == tag.lower():
			self.body = True
		elif "img" == tag:
			self.flag = 1
			self.attrs = attrs
		elif "a" == tag:
			self.flag = 2
			self.attrs = attrs 
		
	def handle_endtag(self, tag):
		if "body" == tag.lower():
			self.body = False
		elif "img" == tag:
			self.flag = 0
		elif "a" == tag:
			self.flag = 0
			
	def handle_data(self, data):
		if self.body == False:
			return
		if self.flag == 1:
			for item in self.attrs:
				if item[0] == "src":
					picPath = item[1]
					if not picPath.startswith("http"):
						picPath = urljoin(self.currentURL, picPath)
					if picPath.startswith("http:"):
						self.picturePaths.add(picPath)
		elif self.flag == 2:
			for item in self.attrs:
				if item[0] == "href":
					nextURL = item[1]
					if not nextURL.startswith("http"):
						nextURL = urljoin(self.currentURL, nextURL)
					if nextURL.startswith("http:"):
						self.nextURLs.append(nextURL)
	def start_grab(self):
		while len(self.picturePaths)<self.maxNumber and len(self.nextURLs)>0:
			try:
				print len(self.picturePaths)
				self.currentURL = self.nextURLs.pop(0)
				if self.currentURL in self.visited:
					continue
				else:
					self.visited.add(self.currentURL)
			
				html = urllib.urlopen(self.currentURL).read()
				self.reset()
				self.feed(html)
				self.close()
			except UnicodeDecodeError, e:
				pass
			except HTMLParseError, e:
				pass
			except IOError, e:
				pass
			
def ispicname(picname):
	index= picname.rfind(".")
	if index == -1:
		return False
	ext = picname[index:]
	if ext.lower() in (".jpg", ".jpeg", ".png", ".bmp"):
		return True
	return False
	
if __name__ == "__main__":
	parse = argparse.ArgumentParser(prog="GrabPicture", description="Grab picture from intenet.")
	parse.add_argument("s", help="a url, the start point")
	parse.add_argument("-n", "--number", dest="number", type=int, default=100, help="how many picture you want to grab")
	parse.add_argument("-o", dest="outDirectory", default="output", help="output directory")
	args = parse.parse_args()
	print 'Start to grab pictures from %s' % args.s
	pictureGraber = PictureGraber(args.s, args.number)
	pictureGraber.start_grab()
	for pic in pictureGraber.picturePaths:
		print pic
	if len(pictureGraber.picturePaths) >= args.number:
		print 'Sucess: Grab %s' % args.number
	else:
		print 'Fail: Grab %s' % len(pictureGraber.picturePaths)
		
	outDirectory = os.path.abspath(args.outDirectory)
	
	if not os.path.isdir(outDirectory):
		try:
			os.mkdir(outDirectory)
		except:
			print "can't create output directory, failed"
			sys.exit()
	print "start download"
	for picPath in pictureGraber.picturePaths:
		picname = picPath[picPath.rfind("/")+1:]
		picname = os.path.join(outDirectory, picname)
		if ispicname(picname):
			print "download %s to %s" % (picPath, picname)
			open(picname, "wb").write(urllib.urlopen(picPath).read())
	print "OK"
	
