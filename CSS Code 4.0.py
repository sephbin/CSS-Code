master_css = r'''
"bed" in d["class"]{ceiling: other; floor: good carpet; door: black; }
"other" in d["class"]{ceiling: other; floor: ASas carpet; door: dAD; }
"A" in d["class"]{X:1; Y:call(http://www.google.com); Z:3;}|
"B" in d["class"]{X:4; Y:5; Z:6;}
"B" in d["class"] and  "ROOF" in d["class"]{Z:GLASS CEILING; k:call(http://www.gooqdgle.com)}
re.search(r"\bB\b",d["class"]){X:10; Y:11; Z:12;}
d["area"] > 300{hello:world;}
'''

# master_css = r'''
# "B" in d["class"] and  "ROOF" in d["class"]{Z:GLASS CEILING; k:call(http:\\www.google.com)}
# '''

import re
def css_unpacking(css):
	try:
		file = open(css, mode='r')
		css = file.read()
		file.close()
	except: pass

	# Format file and sort into Master CSS dictionary

	css_data = css.replace('\n', '').replace('\t', '').replace('}', '}<!css-split!>')#.replace(' ', '')
# 	print(css_data)
	# [^][^{]+{[^}]+?}
	css_data = css_data.split("<!css-split!>")

	css_data = css_data[:-1]


	cssarray = []
	for entry in css_data:
		regex = re.search('^(.+?){(.+?)}$', entry, re.IGNORECASE)

		search = regex.group(1)
# 		print(search)
		style = regex.group(2)
# 		print(style)
		style = style.split(";")
		sdict = {}
		for s in style:
			try:
				kv = s.split(":",1)
# 				print(kv)
				sdict[kv[0]] = kv[1]
			except: pass
		outdict = {"search": search, "style": sdict}
		cssarray.append(outdict)
	return cssarray

cssarray = css_unpacking(master_css)
# print(cssarray)

obs = [
{"class":"A ", "level":"", "star":"1", "area":500, "walls": "yellow", "door":"orange"},
{"class":"B", "level":"10", "star":"", "area":150, "walls": "red", "door":"wood"},
{"class":"B ROOF", "level":"10", "star":"", "area":150, "walls": "red", "door":"wood", "Z":"LAVA"}
]

import requests
from requests.exceptions import HTTPError

finishedobs = []
for ob in obs:

    d = ob
    outdict = {}
    for css_item in cssarray:
        try:
#             print(css_item["search"],',',eval(css_item["search"]))
            if eval(css_item["search"]):
                
                outdict.update(css_item["style"])
                for k, v in css_item["style"].items():
                    if 'call' in v:
                        
                        regex = re.search('(?<=\().+?(?=\))', v)
                        link = regex.group(0)
                        
                        try:
                            r = requests.get(link)
                            
#                             r = requests.get('https://///',params=[('/', '///')],)

#                             v = r.json()
#                             v = r.content

                            call_dic = {k:link}
                            outdict.update(call_dic)

                        except HTTPError as http_err:
                            v = (f'HTTP error occurred: {http_err}')
                            call_dic = {k:v}
                            outdict.update(call_dic)
                            
                        except Exception as err:
                            v = (f'Error occurred: {err}')
                            call_dic = {k:v}
                            outdict.update(call_dic)

        except Exception as e: 
 
            pass


    outdict.update(ob)
 
    finishedobs.append(outdict)


print('\n',finishedobs)