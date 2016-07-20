from pytube import YouTube
import os

def read_links(pathRead):
	''' Preprocess links '''	
	f = open(pathRead, 'r')

	linkList = f.readlines()

	linkList = linkList[0].split(', ')
	linkList[0] = linkList[0].replace("[", "")
	linkList[-1] = linkList[-1].replace("]\n", "")
	linkList = [l[1:-1] for l in linkList]
	return linkList

def download_links(linkList, pathWrite):
	''' Download the links '''
	name_num = 0

	for l in linkList:
		y = YouTube(l)
		y.set_filename(str(name_num))
		video = y.get('mp4', '720p')
		video.download(pathWrite)
		name_num += 1

if __name__ == "__main__":
	links = read_links('linkList.txt')
	download_links(links, '.')
	
