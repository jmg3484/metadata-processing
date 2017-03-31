import sys, io
import plotly

class ImageFile:
	def __init__(self, name):
		self.name = name
		self.attributes = {}

if (len(sys.argv) != 2):
	print("Usage: " + sys.argv[0] + " [report-file]")
	sys.exit(1)

imageFileList = []
interestingAttributes = { 
	'Application': {},
	'Author': {},
	'Creator': {},
	'Make': {},
	'Software': {}
}

file = io.open(sys.argv[1], "r")
newFile = None
for line in file:
	if ":" not in line and len(line) > 1:
		if newFile:
			imageFileList.append(newFile)
		fileName = str(line)
		fileName = fileName.rstrip()
		newFile = ImageFile(fileName)
	elif len(line) > 1:
		attribute = str(line.split(":")[0])
		attribute = attribute.rstrip()
		value = str(line.split(":")[1])
		newFile.attributes[attribute] = value	
		if attribute in interestingAttributes.keys():
			if value in interestingAttributes[attribute]:
				interestingAttributes[attribute][value] += 1
			else:
				interestingAttributes[attribute][value] = 1

for attribute in interestingAttributes.keys():
	fig = { 
		'data': [{'labels': interestingAttributes[attribute].keys(),
			'values': interestingAttributes[attribute].values(),
			'type': 'pie'}], 
		'layout': {'title': attribute}
	}
	plotly.offline.plot(fig, filename=attribute + '.html')
