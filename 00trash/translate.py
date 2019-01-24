import db_mysql
import json
import urllib2
import urllib
import socket


def readContent(sourceLang, targetLang, sourceText):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

	site = "https://translate.googleapis.com/translate_a/single?client=gtx&sl="+sourceLang+"&tl="+targetLang+"&dt=t&q="+sourceText;

	req = urllib2.Request(site, headers=hdr)

	while True:
		try:
		    page = urllib2.urlopen(req, timeout=10)
		    print "success";
		    break;
		except urllib2.URLError, e:
			print "URL ERROR";
		except socket.timeout:
			print "TIMEOUT";
		except Exception:
		    print "EXCEPTION";
		else:
			print "ELSE";

	content = page.read()
	return content;

sql = "SELECT * FROM mining_dict_en WHERE id > 5910";
db_mysql.executeSql(sql);
result = db_mysql.fetch();
i = 0;
for row in result:
	word = row[1].replace("_"," ");
	word = urllib.quote(word);
	
	translated = readContent('id','en',word);

	translated = translated.split('"')[1];
	translated = translated.replace("'","");
	sql = "UPDATE mining_dict_en SET word='" + translated + "' WHERE id=" + str(row[0]);
	# print sql;
	db_mysql.executeSql(sql);
	print str(row[0]);
	i = i + 1;
	if(i == 10):
		db_mysql.commit();
		i = 0;