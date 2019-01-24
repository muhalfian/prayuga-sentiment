from nltk.tokenize import word_tokenize
import needed.db_mysql as db_mysql
import re
import json
from pprint import pprint;

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    #r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

# cut sentence become words by space
def tokenize(s):
    # check the group word (one meaning word but with space) => "warga china"
    daftar_group_word = [];

    the_group_words = db_mysql.getMemoryGroupWord();
    for word in the_group_words:
      daftar_group_word.append(word[0]);

    the_group_words = db_mysql.getOtherMemoryGroupWord();
    for word in the_group_words:
      daftar_group_word.append(word[0]);

    s_temp = [];
    i = 0;
    next_split = 0;
    for group_word in daftar_group_word:
      if(i==0):
        s = s.split(group_word);
      else:
        s = s[next_split].split(group_word);

      if(len(s) > 1):
        s_temp.append(s[0]);
        s_temp.append(group_word);
        next_split = 1;
      else:
        next_split = 0;

      if(i == len(daftar_group_word) - 1):
          s_temp.append(s[next_split]);
      i = i+1;

    arr = [];
    for s in s_temp:
      if s in daftar_group_word:
        arr.append(s);
      else:
        ss = tokens_re.findall(s);
        for w in ss:
          arr.append(w);
    return arr;

# preprocess sentence
def preprocess(s, lowercase=False):
    s = s.lower();
    tokens = tokenize(s);
    # print tokens;
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# remove stop word
def checkStoplist(word):
	result = db_mysql.existStoplist(word);
	if result == None:
		return True;
	else:
		return False;

# Remove space on url "http://contoh.com/menjadi- manusia-damai" => "http://contoh.com/menjadi-manusia-damai"
def removeSpaceOnUrl(content):
  s = content.split('http');
  part_content = [];
  if(len(s) > 1):
    part_content.append(s[0]);

    part_url      = s[1].split('/');
    part_url_real = [];
    i = 0;
    for part in part_url:
      if(i < len(part_url)-1):
        part = part.replace(" ","");
      if(i==0):
        part_url_real.append(""+part);
      else:
        part_url_real.append("/"+part);
      i = i+1;
    part_url = ''.join(part_url_real);
    part_url = "http"+part_url;
    part_content.append(part_url);

    content = ''.join(part_content);
    # print content;
  return content;

def do(content):
    content = re.sub('\.+','.',content);
    content = re.sub('\,+',',',content);
    content = content.replace("/ ","/");
    content = content.replace("www. ","www.");
    content = removeSpaceOnUrl(content);
    content = re.sub(r'RT', '', content);
    content = re.sub(r'http\S+', '', content, flags=re.MULTILINE);
    content = re.sub(r'@([A-Za-z0-9_]+)', '', content, flags=re.MULTILINE);
    content = re.sub(r'pic.twitter.com/\S+', '', content, flags=re.MULTILINE);
    content = content.replace("?"," ? ");
    content = content.replace("-"," ");
    content = content.replace("/"," ");
    content = content.replace("."," . ");
    content = content.replace(","," , ");
    content = re.sub(r'[^a-z0-9.,?# -]', ' ', content, flags = re.IGNORECASE|re.MULTILINE)
    content = re.sub(" \d+", " ", content)
    content = re.sub(r'( +)', ' ', content, flags = re.IGNORECASE|re.MULTILINE)

    res = [];
    for word in preprocess(content,True):
    	 if checkStoplist(word):
    		  res.append(word);
    return res;

# for record rule work
def recordCounting(v):
    arr_word    = '';
    arr_counted = '';
    arr_score   = '';
    i = 0;
    for word in v['words']:
        if(i == 0):
            arr_word    = arr_word + word['word']+"|"+str(word['type'])+"|"+str(word['value']);
            arr_counted = arr_counted + v['counted'][i];
            arr_score   = arr_score + str(v['score'][i]);
        else:
            arr_word = arr_word+";"+word['word']+"|"+str(word['type'])+"|"+str(word['value']);
            arr_counted = arr_counted +";"+ v['counted'][i];
            arr_score   = arr_score +";"+ str(v['score'][i]);
        i = i+1;

    roleGroup = str(json.dumps(v['roleGroup']));

    result = {
        'arr_word'   : arr_word,
        'arr_counted': arr_counted,
        'arr_score'  : arr_score,
        'role_group' : roleGroup
    };
    return result;
