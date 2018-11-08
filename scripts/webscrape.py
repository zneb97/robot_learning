"""
File to pull and shape images for use in training and validation dataset
for Olin's CompRobo robot learning project

Outputs a number of images scraped from Google that have been
resized. 

DISCONTINUED due to generating our own images in known environment

TODO:
Make xml labels for ball is there or not
Expand background randomly then use hough transform to locate ball
Fake and tune cmd vels
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
import time

class webScraper():

    def __init__(self, term, img_count =100, direct='dataSet/'):
        self.term = term
        self.img_count = img_count
        self.dir = direct

        self.img_size = 300


    def get_soup(self, url,header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


    def reshape(self, loc):
        """ 
        Reshape an image to a standard size for use in training
        """
        img = Image.open(loc)
        img = img.resize((self.img_size, self.img_size))
        return img


    def run(self):
        image_type="Action"
        query= self.term.split()
        query='+'.join(query)
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url,header)
        
        #Setup
        if not os.path.exists("dataSet/"):
            os.mkdir("dataSet/")
        if not os.path.exists("dataSet2/"):
            os.mkdir("dataSet2/")


        ActualImages=[]
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))


        #Grab and process each image
        for i , (img , Type) in enumerate( ActualImages[0:self.img_count]):
            print(i)
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req, timeout=3).read()
                f = open(os.path.join(self.dir, "img" + "_"+ str(i)+"."+Type), 'wb')
                f.write(raw_img)
                f.close()

                img = self.reshape("dataSet/img" + "_"+ str(i)+"."+Type)
                img.save("dataSet2/img" + "_"+ str(i)+".png","PNG")

            except Exception as e:
                print("Cannot save #%i" %i)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--term', default= "soccer ball", type=str)
    parser.add_argument('-n', '--count', default=100, type=int)
    parser.add_argument('-d', '--dir', default='dataSet/', type=str)
    args = parser.parse_args()

    ws = webScraper(args.term, args.count, args.dir)
    ws.run()