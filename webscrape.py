"""
File to pull and shape images for use in training and validation dataset
for Olin's CompRobo robot learning project

Outputs a number of images scraped from Google that have been
resized. 
"""

from bs4 import BeautifulSoup
from sys import argv
from PIL import Image
import requests
import re
import urllib2
import glob, os
import argparse
import sys
import json

class webScraper():

	def __init__(self, img_size = 300, img_count = 100, direct='/home/bziemann/olin/dataSet'):
		self.img_size = img_size
		self.img_count = img_count
		self.dir = direct


	def get_soup(url,header):
	    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


	def reshape(self, img):
		"""	
		Reshape an image to a standard size for use in training
		"""
		im = Image(img)
		return im.resize((self.img_size, self.img_size))


	def run(self):

		parser = argparse.ArgumentParser(description='Scrape Google images')
		parser.add_argument('-s', '--term', default=self.search, type=str)
		parser.add_argument('-n', '--count', default=self.img_count, type=int)
		parser.add_argument('-d', '--dir', default=self.dir, type=str, help='save directory')
		args = parser.parse_args()
		query = args.term
		max_images = args.count
		save_directory = args.dir
		image_type="Action"
		query= query.split()
		query='+'.join(query)
		url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
		header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		soup = get_soup(url,header)

		ActualImages=[]
		for a in soup.find_all("div",{"class":"rg_meta"}):
		    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		    ActualImages.append((link,Type))
		for i , (img , Type) in enumerate( ActualImages[0:max_images]):
		    try:
		        req = urllib2.Request(img, headers={'User-Agent' : header})
		        raw_img = urllib2.urlopen(req).read()
		        img = reshape(raw_img)
		        if len(Type)==0:
		            f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
		        else :
		            f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
		        f.write(img)
		        f.close()
		    except Exception as e:
		        print "could not load : "+img
		        print e

if __name__ == '__main__':
    ws = webScraper()
    ws.run()