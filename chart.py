import sys, io

# pip install plotly

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

# Report files are formatted with the name of the file on one line,
# then that files attributes directly under. Each file section is 
# separated by a blank line. The file is initialized when we read a
# line lacking a colon, and then all of its attributes are read in.
# If the attribute is "interesting" (worth graphing, just based on
# what I thought should've been looked into), increment the number
# of times we've seen that value in the attribute dictionary, or
# just insert it if we've never seen it before.

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

# Generate a chart using plotly for each interesting attribute.

for attribute in interestingAttributes.keys():
	fig = { 
		'data': [{'labels': interestingAttributes[attribute].keys(),
			'values': interestingAttributes[attribute].values(),
			'type': 'pie'}], 
		'layout': {'title': attribute}
	}
	plotly.offline.plot(fig, filename=attribute + '.html')
