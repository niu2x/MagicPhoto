# -*- coding:utf-8 -*-
import argparse
import os
import sys
reload(sys)
from PIL import Image
import glob
sys.setdefaultencoding('utf8')

def find_proper_tile(tiles, value):
	result = tiles[0]
	for i in tiles:
		if i[1] == value:
			result = i
			break
		elif i[1] > value:
			if i[1] - value < value - result[1]:
				result = i
			break
		else:
			result = i
	return result
def calculate_average_color(image):
	size = image.size
	r = 0
	g = 0
	b = 0
	for x in range(size[0]):
		for y in range(size[1]):
			color = image.getpixel((x,y))
			r += color[0]
			g += color[1]
			b += color[2]
	pixelsNumber = size[1] * size[0]
	r /= pixelsNumber
	g /= pixelsNumber
	b /= pixelsNumber
	return (r+g+b)/3

def safe_load_img(filename):
	try:
		img = Image.open(filename)
	except IOError, e:
		print "can't open img %s " % filename
		sys.exit()
	return img.convert("RGB")

def load_tile(tilePath):
	size = None
	tiles = []
	for item in glob.glob(tilePath):
		img = safe_load_img(item)
		if size == None:
			size = img.size
		else:
			if size != img.size:
				print "tile's size aren't same"
				sys.exit()
		tiles.append((img, calculate_average_color(img)))
	def img_cmp(imga, imgb):
		if imga[1] > imgb[1]:
			return 1
		elif imga[1] == imgb[1]:
			return 0
		else:
			return -1
	tiles.sort(cmp=img_cmp)
	if size == None:
		print "need at least one tile."
		sys.exit()
	return tiles, size

def load_source(source):
	return safe_load_img(source)

def make_output(tiles, sourceImg):
	tileSize = tiles[0][0].size
	sourceSize = sourceImg.size
	xStep = sourceSize[0] / tileSize[0]
	yStep = sourceSize[1] / tileSize[1]
	for x in range(xStep):
		for y in range(yStep):
			box = (x*tileSize[0], y*tileSize[1], (x+1)*tileSize[0], (y+1)*tileSize[1])
			sourceTile = sourceImg.crop(box)
			averageValue = calculate_average_color(sourceTile)
			replaceTile = find_proper_tile(tiles, averageValue)[0]
			sourceImg.paste(replaceTile, box)
	return sourceImg
if __name__ == "__main__":
	parse = argparse.ArgumentParser(prog="MagicPhoto", description="resize picture.")
	parse.add_argument("source", help="source photo to be processed")
	parse.add_argument("tilePath", help="path of tiles with same size")
	parse.add_argument("output", help="a url, the start point")
	args = parse.parse_args()
	tiles, tileSize = load_tile(args.tilePath)
	print tileSize
	for i in tiles:
		print i[0], i[1]
	sourceImg = load_source(args.source)
	sourceImgSize = sourceImg.size
	if sourceImgSize[0] % tileSize[0] != 0 or sourceImgSize[1] % tileSize[1] != 0:
		print "size of source isn't integer times of tile's size."
		sys.exit()
	outputImg = make_output(tiles, sourceImg)
	try:
		outputImg.save(args.output)
	except IOError, e:
		print "can't save %s" % args.output
		
