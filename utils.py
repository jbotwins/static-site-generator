# Importing dependencies
import sys
import os
import readline
import glob
import json
from jinja2 import Template

def directoryStatus(folder, fileNames):
	print('The current state of the', folder, 'directory is:')
	if len(fileNames) > 1:
		print(fileNames)
	else:
		print('The', folder, 'directory is empty! :)')

def deleteFileList(files):
	for file in files:
		os.remove(file)

def getAdditionalMetaData(file, contentMetaData):
	name = file.split('/')[1]
	# print('22',name)
	for item in contentMetaData["pages"]:
		# print('24',item)
		if item['Filename'] == name:
			return item

def readJsonData():
	data = open('contentMetaData.json', ).read()
	jsonData = json.loads(data)
	# print('31',jsonData)
	return jsonData
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
# Build the pages
def buildPages(contentMetaData, inputDir, outputDir):
	inputFiles = glob.glob('content/*.*')
	print('37', inputFiles)

	for item in inputFiles:
		additionalMetaData = getAdditionalMetaData(item, contentMetaData)
		item_html = open(item).read()
		if additionalMetaData is not None:
			print('42',additionalMetaData)
			print('43', len(additionalMetaData))
			title = additionalMetaData['Title']
			date = additionalMetaData['Date']
			author = additionalMetaData['Author']
			me = additionalMetaData['Filename']

			template_html = open('templates/base.html').read()
			template = Template(template_html)

			finished_item = template.render(
				title=title,
				date=date,
				author=author,
				content=item_html,
				me=me,
				pages=contentMetaData,
				)
			# print('54')
			# print('output')
			output = outputDir + '/' + additionalMetaData['Filename']
			open(output, 'w+').write(finished_item)
	print('built all the pages!')

def buildSite():
### Cleansing the output directory ###
	print('running buildSite function')
	outputDir = 'docs'
	outputFiles = glob.glob(outputDir+'/'+'*.html')
	# print('73')
	# print(outputFiles)
	# Print current status of /docs directory.
	directoryStatus(outputDir, outputFiles)

	# Remove all HTML files in /docs directory.
	deleteFileList(outputFiles)
### Additonal Content MetaData & Build Preparation ###
	#template = 'templates/base.html' ### DELETE?

	inputDir = 'content'
	contentMetaData = readJsonData()
	# print('84',contentMetaData)
### Generating the Output ###
	buildPages(contentMetaData, inputDir, outputDir)

def newPage():
	print('running newPage function')
	placeHolderContent = '''
		<h1>New Content!</h1>
    	<p>New content...</p>
	'''
	placeHolderMetaData = {
			'Title': 'Placeholder Title',
			'Date': 'Today\'s Date',
			'Author': 'Author Name',
			'Filename': 'new_content_page.html',
		}
	open('content/new_content_page.html', 'w+').write(placeHolderContent)
	metaCurrent = open('contentMetaData.json', 'r').read()
	jsonData = json.loads(metaCurrent)
	# print('100')
	# print(jsonData)
	jsonData.append(placeHolderMetaData)
	# print('103')
	# print(jsonData)
	open('contentMetaData.json', 'w+').write(jsonData)
	buildSite()

def main():
	command = sys.argv
	print('running main function')
	try:
		# print(command)
		# print('Recieved the following argument: ' + command[1])
		if command[1] == 'build':
			buildSite()
			print('I built the site!')
			# return True
		elif command[1] == 'new':
			newPage()
			print('I added a new page to the site!')
			# return True
		else:
			print('''
Recieved the following argument: \'''' + command[1] + '''\'
Please specify \'new\' or \'build\'
			''')
	except:
		print('''
No argument recieved:
Please specify \'new\' or \'build\'
			''')