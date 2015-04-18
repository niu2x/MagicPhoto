# -*- coding:utf-8 -*-
import argparse
import os
import sys
reload(sys)
from PIL import Image
import glob
sys.setdefaultencoding('utf8')
	
if __name__ == "__main__":
	parse = argparse.ArgumentParser(prog="ResizePicture", description="resize picture.")
	parse.add_argument("path", help="a url, the start point")
	parse.add_argument("width", type=int, help="a url, the start point")
	parse.add_argument("height", type=int, help="a url, the start point")
	parse.add_argument("output", help="a url, the start point")
	args = parse.parse_args()

	if os.path.isfile(args.output):
		print "%s is a file" % args.output
		sys.exit()
	if not os.path.exists(args.output):
		os.mkdir(args.output)
	for item in glob.glob(args.path):
		try:
			img = Image.open(item)
		except IOError, e:
			print "can't open file %s " % item
			sys.exit()
		img = img.resize((args.width, args.height))
		try:
			img.save(os.path.join(args.output, os.path.basename(item)))
		except IOError, e:
			print "can't save file %s " % os.path.join(args.output, os.path.basename(item))
			sys.exit()
	
