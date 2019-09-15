#-*-coding:utf-8-*-
from lxml import etree
import json

ns = {
	'pkg':'http://schemas.microsoft.com/office/2006/xmlPackage', 
	'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}


tree = etree.parse("di-zi-gui.xml")
root = tree.getroot()

content = {}

ps=root.xpath('//w:p', namespaces = ns)

isFirst = True

chapter = {}

for p in ps :
	texts = []
	pinyins = p.xpath('w:r/w:ruby/w:rt/w:r/w:t/text()', namespaces = ns)
	hanzis = p.xpath('w:r/w:ruby/w:rubyBase/w:r/w:t/text()', namespaces = ns)

	for i in range(0, len(pinyins)) :
		texts.append({'text': hanzis[i], 'pinyin': pinyins[i]})

	if len(texts) == 0 : 
		continue
	
	if isFirst : 
		content['title'] = texts
		content['chapters'] = []

	if len(texts) < 8 : 
		chapter['title'] = texts
	else :
		parts = []
		for i in range(0, len(texts), 3) :
			parts.append(texts[i: i + 3])
		chapter['content'] = parts
		content['chapters'].append(chapter)
		chapter = {}


	isFirst = False

output = json.dumps(content, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ':'))
print(output)


