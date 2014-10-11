import sys
import re
import subprocess
import os

if(len(sys.argv) != 2):
	print('usage: downloader.py dirName')
	exit(1)

dirName = sys.argv[1]
fileNames = os.listdir('./' + dirName)

r = re.compile('http://media.wizards.com/images/magic/tcg/products/.*png')

downloadList =[]
for htmlFile in fileNames:
	print(htmlFile)
	for line in open(dirName + htmlFile, 'r'):
		m = r.search(line)
		if(m != None):
			downloadList.append(m.group(0))

fileNumberCount = 0
for cardNum in downloadList:
	fileNumberCount += 1
	fileName = "{0:03d}".format(fileNumberCount) + '.png'
	# url = 'http://gatherer.wizards.com/Handlers/Image.ashx?' + cardNum + '&type=card'
	url = cardNum
	print(url)
	command = ['curl', '-o', fileName, url]
	subprocess.call(command)
