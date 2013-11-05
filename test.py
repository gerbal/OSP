import semester
import glob
import os

for i in glob.glob(os.getcwd() + "/testpool/*.odt"):
	file = open( i,"rb")
	print i
	semester.ParseFile(file)
