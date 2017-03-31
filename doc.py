import io, sys, subprocess

class ImageFile:
	def __init__(self, name):
		self.name = name
		self.attributes = {
			"Application":"",
			"App Version":"",
			"Author":"",
			"Comments":"",
			"Company":"",
			"Create Date":"",
			"Creator":"",
			"Keywords":"",
			"Last Modified By":"",
			"Security":"",
			"Software":"",
			"Zip Bit Flag":"",
			"Zip CRC":"",
			"Zip File Name":"",
			"Zip Required Version":"",
		}

class ImageFileList:
	list = []
	counter = -1

if (len(sys.argv) != 2):
	print("Usage: " + sys.argv[0] + " [in-file]")
	sys.exit(1)

fileList = ImageFileList()

file = io.open(sys.argv[1], "r")
for line in file:
	fileName = str(line)
	fileName = fileName.rstrip()
	newFile = ImageFile(fileName)
	tool_output = subprocess.check_output(["exiftool", fileName])
	output_lines = tool_output.splitlines()
	for output_line in output_lines:
		attribute = str(output_line.split(":")[0])
		attribute = attribute.rstrip()
		if attribute in newFile.attributes.keys():
			value = output_line.split(":")[1]
			value = value.lstrip()
			newFile.attributes[attribute] = value
	fileList.list.append(newFile)
	fileList.counter += 1
for file in fileList.list:
	print("\n" + file.name)
	for attribute in file.attributes:
		value = file.attributes[attribute]
		if len(str(value)) > 0:
			print(attribute + ": " + value)
