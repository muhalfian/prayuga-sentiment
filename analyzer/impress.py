# -*- coding: utf-8 -*-
import nltk
import needed.db_mysql as db_mysql

from pprint import pprint;

# initial manual code type of word based on database
W_NOUN 		 = 1;
W_VERB 		 = 2;
W_VERB_DI	 = 3;
W_ADJ 		 = 4;
W_PREPOSISI  = 5;
W_KONJUNGSI  = 6;
W_INTERJEKSI = 7;
W_NUMERALIA	 = 8;
W_KEYWORD 	 = 9;
W_ADV 		 = 10;

idApps = None;

# Just route for play the role
# @params Array sentence : list word
# @return Integer value sentiment
def play(sentence,id_apps=None):
	global idApps;
	idApps = id_apps;
	return toRole(sentence);


# The role
# @params Array sentence
# @return Integer value sentiment
def toRole(sentence):
	word_token = sentence;
	# get type and val of the words
	initial_attr_word = initialAttrWord(word_token);

	list_word  = initial_attr_word['list_word'];
	total_word = len(list_word);
	
	# Needed for record rule, for trace the rule work
	record = {}
	record['rule']    = [];
	record['counted'] = ['x'] * total_word;
	record['score']   = [0] * total_word;

	i = 0;
	while (i < total_word):
		#initial word position
		word = {}; 
		word['current'] = list_word[i];
		word['before']  = None;
		word['before2'] = None;
		word['after']   = None;
		word['after2']  = None;
		if (i != 0): 			word['before']  = list_word[i-1]; # if not in first word
		if (i > 1):				word['before2'] = list_word[i-2]; # if not in at least second word
		if (i < total_word-1):  word['after']   = list_word[i+1]; # if not in last word
		if (i < total_word-2):  word['after2']  = list_word[i+2]; # if not in at least second last word
		iCurrent   = i;
		posCurrent = checkPositionWord(iCurrent,total_word);

		record_rule = None;
		# Check verb active
		if (word['current']['type'] == W_VERB):
		 	record_rule = countVerb(word);
		 	i = surgeryRecord(record_rule,record['counted'],record['score'],i);

		# Check verb pasive
		elif (word['current']['type'] == W_VERB_DI):
		 	record_rule = countPassiveVerb(word);
		 	i = surgeryRecord(record_rule,record['counted'],record['score'],i);

		# Check adj
		elif (word['current']['type'] == W_ADJ):
			record_rule = countAdj(word);
			i = surgeryRecord(record_rule,record['counted'],record['score'],i);

		# Check others but not netral
		elif (word['current']['value'] != 0 and (word['current']['type'] != W_PREPOSISI and word['current']['type'] != W_ADV and word['current']['type'] != W_NOUN)):
			record['counted'][i] = 'ss';
			record['score'][i]   = word['current']['value'];

		if (record_rule != None):
			record['rule'].append(record_rule);

		i = i+1;

	var_return = {};
	var_return['sentiment'] = countingScoreForSentiment(sum(record['score']));
	var_return['words']     = list_word;
	var_return['score']     = record['score'];
	var_return['counted']   = record['counted'];
	var_return['roleGroup'] = [];
	for rule in record['rule']:
		var_return['roleGroup'].append(rule[-1]['progress']);
	var_return['recordRuleWork'] = record['rule'];
	
	return var_return;
	

# get type and val of the words
# @params Array words
# @return Array mixed
def initialAttrWord(word_token):
	list_word  = [];

	j = 0;
	len_word_token = len(word_token);
	for word in word_token:
		# if there "di" that seperate with verb, like -> di tahan = ditahan, so become verb_di
		if (word == "di"  and  j < len_word_token-1):
			word_next = checkSentimentalWord(word_token[j+1]);
			if (word_next[2] == W_VERB):
				word_token[j+1] = "di"+word_token[j+1];
			j = j+1;
			continue;

		word_with_attr = checkSentimentalWord(word);
		the_word       = {'word':word, 'type':word_with_attr[2], 'value':word_with_attr[3]};
		list_word.append(the_word);
		j = j+1;

	v_return = {};
	v_return['list_word'] = list_word;
	return v_return;


# Get info type and value sentiment of word
# @params String word
# @return Array
def checkSentimentalWord(word):
	# get info data of the word, the sentiment and type
	result = db_mysql.existSentimentalWord(word);
	# if not in memory db, insert into unknown word
	if result == None:
		result = [];
		result.append(0);
		result.append(word);
		# result.append(checkWordTypeFromOtherCorpus(word));
		result.append('unknown');
		result.append(0);
		db_mysql.insertUnknownWord(word);
	
	# get info main object based on case and set value of sentiment to words
	objord = db_mysql.existSentimentalWordMainObject(word,idApps);
	result = list(result);
	if (objord != None):
		result[3] = float(objord[2]);
		if(result[2] == 'unknown'):
			result[2] = W_NOUN;

	return result;


# Get info type of word from other corpus (kbbi) if there are not in main-corpus
# @params String word
# @return Integer type word
def checkWordTypeFromOtherCorpus(word):
	result = db_mysql.existOtherKamus(word);
	if result == None:
		return 'unknown';
	else:
		return result[2];


# Count the logic for sentiment
# @params Integer x, Integer y, String type_logic
# @return Integer value setiment
def countLogic(x, y, type_logic):
	result = 0;
	if  (x==0): result = y;
	elif(y==0): result = x;
	else:
		if(type_logic == 'p ∧ q'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = -1;
		elif(type_logic == 'p ∨ q'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = 1;
			elif (x==-1 and y==1 ):	result = 1;
			elif (x==-1 and y==-1): result = -1;
		elif(type_logic == 'p → q'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = 1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == 'p ↔ q'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == '~(p ∨ q)'):
			if 	 (x==1  and y==1 ):	result = -1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == '~p → ~q'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = 1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == '~(~p → ~q)'):
			if 	 (x==1  and y==1 ):	result = -1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = 1;
			elif (x==-1 and y==-1): result = -1;
		elif(type_logic == 'p'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = 1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = -1;
	return result;


# Count score for sentiment
# @params Integer score
# @return Integer
def countingScoreForSentiment(score):
	if (score > 0):
		return 1;
	elif (score < 0):
		return -1;
	else:
		return 0;


# Check position word on sentence
# @params Integer CurrentI, Integer TotalWord
# @return Integer Position, 1=First, 2=Middel, 3=Last
def checkPositionWord(iCurrent, total_word):
	if(iCurrent == 0):
		return 1; #first
	elif(iCurrent == total_word-1):
		return 3; #last
	else:
		return 2; #middle


# Split the sentence by comma or point
# @params Array word of sentence
# @return Array group of word split by comma or point
def splitSentence(sentence):
	groupSentence = [];
	groupWord = [];
	for word in sentence:
		groupWord.append(word);
		if(word == ',' or word == '.'):
			groupSentence.append(groupWord);
			groupWord = [];

	groupSentence.append(groupWord);

	valSentiment = 0;
	for sentence in groupSentence:
		sentiment = toRole(sentence)
		valSentiment = valSentiment + sentiment;
	return countingScoreForSentiment(valSentiment);


# For rule active verb
def countVerb(word):
	# Just for record progress rule work
	progress_rule = [];
	progress     = [None] * 5;
	# as default score is value of current word
	score        = word['current']['value'];
	# Just for record progress rule work
	recordProgressRule(progress_rule,'current','IT_SELF',score,word);
	# if there are precious on after word
	if (word['after'] != None):
		if (word['after']['type'] == W_NOUN):
			score = countLogic(score,word['after']['value'],'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'after','p ↔ q',score,word);
			if (word['after2'] != None and word['after2']['type'] == W_ADJ):
				score = countLogic(score,word['after2']['value'],'p ∧ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after2','p ∧ q',score,word);

		elif (word['after']['type'] == W_ADJ):
			# if after is W_ADJ and after2 is W_NOUN
			if (word['after2'] != None and word['after2']['type'] == W_NOUN):
				score = countLogic(score,word['after2']['value'],'p ↔ q');
				score = countLogic(score,word['after']['value'],'p ∧ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after2','p ↔ q',score,word);
				recordProgressRule(progress_rule,'after','p ∧ q',score,word);
			else:
				score = countLogic(score,word['after']['value'],'p ∧ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after','p ∧ q',score,word);

	# if there are precious on before word
	if (word['before'] != None):
		if (word['before']['type'] == W_ADV or word['before']['type'] == W_PREPOSISI):
			scoreBF = score;
			score   = countLogic(word['before']['value'],score,'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ↔ q',score,word);
			if (word['before2'] != None and word['before2']['type'] == W_NOUN):
				if ((word['current']['value'] == 1) and (word['after'] != None and word['after']['value'] == 1)):
					canAccess = 1;
					if(word['after2'] != None and word['after2']['value'] != 1):
						canAccess = 0;
					if(canAccess == 1):
						logicNP = countLogic(word['before2']['value'], word['before']['value'], 'p ↔ q');
						score = countLogic(logicNP, scoreBF, 'p ↔ q');	
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'before2','p ↔ q',logicNP,word,2,[1,1,0,0,0],[None]*5);
						recordProgressRule(progress_rule,'before','p ↔ q',score,word,2,[1,1,1,1,1],list(progress_rule[-1]['progress']));

				if (word['after'] == None and word['after2'] == None):
					score = countLogic(word['before2']['value'], score, 'p ↔ q');
					# Just for record progress rule work
					recordProgressRule(progress_rule,'before2','p ↔ q',score,word);
				
		elif (word['before']['type'] == W_NOUN):
			scoreBF = score;
			score   = countLogic(word['before']['value'],score,'p ∧ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ∧ q',score,word);
			if ((word['current']['value'] == 1) and (word['after'] != None and word['after']['value'] == 1)):
				canAccess = 1;
				if(word['after2'] != None and word['after2']['value'] != 1):
					canAccess = 0;
				if(canAccess == 1):
					score = countLogic(word['before']['value'], scoreBF, 'p ↔ q');
					if(word['before2'] != None):
						if(word['before2']['type'] == W_ADV or word['before2']['type'] == W_PREPOSISI):
							logicNP = countLogic(word['before2']['value'], word['before']['value'], 'p ↔ q');
							score = countLogic(logicNP, scoreBF, 'p ↔ q');	
							# Just for record progress rule work
							del progress_rule[-1];
							recordProgressRule(progress_rule,'before2','p ↔ q',logicNP,word,2,[1,1,0,0,0],[None]*5);
							recordProgressRule(progress_rule,'before','p ↔ q',score,word,2,[1,1,1,1,1],list(progress_rule[-1]['progress']));
							
			elif(word['before2'] != None and (word['before2']['type'] == W_ADV or word['before2']['type'] == W_PREPOSISI)):
				score = countLogic(word['before2']['value'], score, 'p ↔ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'before2','p ↔ q',score,word);

	# pprint(progress_rule);
	return progress_rule;


# For rule passive verb
def countPassiveVerb(word):
	# Just for record progress rule work
	progress_rule = [];
	progress     = [None] * 5;
	# as default score is value of current word
	score        = word['current']['value'];
	# Just for record progress rule work
	recordProgressRule(progress_rule,'current','IT_SELF',score,word);
	# if there are precious on before word
	if (word['before'] != None):
		if (word['before']['type'] == W_ADV or word['before']['type'] == W_PREPOSISI):
			score = countLogic(word['before']['value'], score, 'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ↔ q',score,word);
			if(word['before2'] != None and word['before2']['type'] == W_NOUN):
				score = countLogic(word['before2']['value'], score, 'p ↔ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'before2','p ↔ q',score,word);

		elif (word['before']['type'] == W_NOUN):
			score = countLogic(word['before']['value'], score, 'p ↔ q');	
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ↔ q',score,word);	
			if(word['before2'] != None and (word['before2']['type'] == W_ADV or word['before2']['type'] == W_PREPOSISI)):
				score = countLogic(word['before2']['value'], score, 'p ↔ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'before2','p ↔ q',score,word);
	# if there are precious on after word
	if (word['after'] != None):
		scoreCurrent = score;
		if (word['after']['type'] == W_ADJ):
			score = countLogic(scoreCurrent,word['after']['value'],'p ∧ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'after','p ∧ q',score,word);
			if (word['before'] != None):
				if (word['before']['type'] == W_PREPOSISI or word['before']['type'] == W_ADV):
					if (word['before']['value'] == -1):
						score = countLogic(scoreCurrent,word['after']['value'],'~(p ∨ q)');
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'after','~(p ∨ q)',score,word);
						if(word['before2'] != None):
							if(word['before2']['type'] == W_NOUN):
								if(word['before2']['value'] == -1):
									score = countLogic(scoreCurrent,word['after']['value'],'p ↔ q');
									# Just for record progress rule work
									del progress_rule[-1];
									recordProgressRule(progress_rule,'after','p ↔ q',score,word);

			if(word['after2'] != None and word['after2']['type'] == W_NOUN):
				scoreCurrent = score;
				score = countLogic(scoreCurrent,word['after2']['value'],'p ∧ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after2','p ∧ q',score,word);

				if(word['before'] != None):
					if(word['before']['type'] == W_PREPOSISI or word['before']['type'] == W_ADV):
						if(word['before']['value'] == -1):
							if(word['current']['value'] == -1):
								score = -1;
								# Just for record progress rule work
								del progress_rule[-1];
								recordProgressRule(progress_rule,'after2','ALLNE',score,word);
								if(word['before2'] != None):
									if(word['before2']['type'] == W_NOUN):
										if(word['before2']['value'] == -1):
											score = countLogic(scoreCurrent,word['after2']['value'],'p ∧ q');
											# Just for record progress rule work
											del progress_rule[-1];
											recordProgressRule(progress_rule,'after2','p ∧ q',score,word);
										else:
											score = -1;
											# Just for record progress rule work
											del progress_rule[-1];
											recordProgressRule(progress_rule,'after2','ALLNE',score,word);

							else:
								score = countLogic(scoreCurrent,word['after2']['value'],'p ↔ q');
								# Just for record progress rule work
								del progress_rule[-1];
								recordProgressRule(progress_rule,'after2','p ↔ q',score,word);
								if(word['before2'] != None):
									if(word['before2']['type'] == W_NOUN):
										if(word['before2']['value'] == -1):
											score = countLogic(scoreCurrent,word['after2']['value'],'ALLPO-DEPOPO');
											# Just for record progress rule work
											del progress_rule[-1];
											recordProgressRule(progress_rule,'after2','ALLPO-DEPOPO',score,word);

		elif (word['after']['type'] == W_NOUN):
			score = countLogic(scoreCurrent,word['after']['value'],'p ∧ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'after','p ∧ q',score,word);
			if (word['before'] != None):
				if(word['before']['type'] == W_PREPOSISI or word['before']['type'] == W_ADV):
					if(word['before']['value'] == -1):
						score = countLogic(scoreCurrent,word['after']['value'],'~p → ~q');
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'after','~p → ~q',score,word);
						if (word['before2'] != None and word['before2']['type'] == W_NOUN):
							if(word['before2']['value'] == -1):
								score = countLogic(scoreCurrent,word['after']['value'],'p ∧ q');
								# Just for record progress rule work
								del progress_rule[-1];
								recordProgressRule(progress_rule,'after','p ∧ q',score,word);
					else:
						score = countLogic(scoreCurrent,word['after']['value'],'p ∧ q');
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'after','p ∧ q',score,word);
						
				elif(word['before']['type'] == W_NOUN):
					score = countLogic(scoreCurrent,word['after']['value'],'p ∧ q');
					# Just for record progress rule work
					del progress_rule[-1];
					recordProgressRule(progress_rule,'after','p ∧ q',score,word);

			if(word['after2'] != None and word['after2']['type'] == W_ADJ):
				score = countLogic(score,word['after2']['value'],'p ∧ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after2','p ∧ q',score,word);
				
	return progress_rule;
	

# For rule adjective
def countAdj(word):
	# Just for record progress rule work
	progress_rule = [];
	progress     = [None] * 5;
	# as default score is value of current word
	score        = word['current']['value'];
	# Just for record progress rule work
	recordProgressRule(progress_rule,'current','IT_SELF',score,word);
	# if there are precious on before word
	if (word['before'] != None):
		if (word['before']['type'] == W_NOUN):
			score = countLogic(word['before']['value'], score, 'p ∧ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ∧ q',score,word);
			if(word['before2'] != None and (word['before2']['type'] == W_ADV or word['before2']['type'] == W_PREPOSISI)):
				score = countLogic(word['before2']['value'], score, 'p ↔ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'before2','p ↔ q',score,word);
		elif (word['before']['type'] == W_ADV or word['before']['type'] == W_PREPOSISI):
			score = countLogic(word['before']['value'], score, 'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before','p ↔ q',score,word);
			if(word['before2'] != None and word['before2']['type'] == W_NOUN):
				score = countLogic(word['before2']['value'], score, 'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'before2','p ↔ q',score,word);

	# if there are precious on after word
	if (word['after'] != None):
		scoreCurrent = score;
		if(word['after']['type'] == W_NOUN):
			score = countLogic(scoreCurrent, word['after']['value'], 'p ↔ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'after','p ↔ q',score,word);
		elif(word['after']['type'] == W_VERB or word['after']['type'] == W_VERB_DI):
			score = countLogic(scoreCurrent, word['after']['value'], 'p ∧ q');
			# Just for record progress rule work
			recordProgressRule(progress_rule,'after','p ∧ q',score,word);
			if(word['before'] != None):
				if(word['before']['type'] == W_ADV or word['before']['type'] == W_PREPOSISI):
					score = countLogic(scoreCurrent, word['after']['value'], 'p ↔ q');
					# Just for record progress rule work
					del progress_rule[-1];
					recordProgressRule(progress_rule,'after','p ↔ q',score,word);
				elif(word['before']['type'] == W_NOUN):
					if(word['before']['value'] == -1):
						score = -1;
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'after','ALLNE',score,word);

			if(word['after2'] != None and word['after2']['type'] == W_NOUN):
				scoreCurrent = score;
				score = countLogic(scoreCurrent, word['after2']['value'], 'p ↔ q');
				# Just for record progress rule work
				recordProgressRule(progress_rule,'after2','p ↔ q',score,word);

				if(word['before'] != None and word['before']['type'] == W_NOUN and word['before']['value'] == -1):
					if(word['before2'] != None and (word['before2']['type'] == W_PREPOSISI or word['before2']['type'] == W_ADV)):
						pass;
					else:
						score = -1;
						# Just for record progress rule work
						del progress_rule[-1];
						recordProgressRule(progress_rule,'after2','ALLNE',score,word);

	return progress_rule;

	
# For record the progress rule
def recordProgressRule(progress_rule,step,logic,score,word,type_record=1,record2_progress=[0]*5,record2_last_progress=[None]*5):
	if(type_record == 1):
		if(len(progress_rule) == 0):
			last_progress = [None] * 5;
		else:
			last_progress = list(progress_rule[len(progress_rule)-1]['progress']);
		progress = last_progress;
		progress[2] = word['current'];
		if (step == "after"):
			progress[3] = word['after'];
		elif (step == "after2"):
			progress[4] = word['after2'];
		elif (step == "before"):
			progress[1] = word['before'];
		elif (step == "before2"):
			progress[0] = word['before2'];

	elif(type_record==2):
		progress = record2_last_progress;
		if(record2_progress[0] == 1):
			progress[0] = word['before2'];
		if(record2_progress[1] == 1):
			progress[1] = word['before'];
		if(record2_progress[2] == 1):
			progress[2] = word['current'];
		if(record2_progress[3] == 1):
			progress[3] = word['after'];
		if(record2_progress[4] == 1):
			progress[4] = word['after2'];

	rule = {};
	rule['progress'] = progress;
	rule['logic']    = logic;
	rule['score']    = score;

	progress_rule.append(rule);


# For get info for the record
def surgeryRecord(record_rule,counted,score,i):
	last_record   = record_rule[-1];
	score[i]      = last_record['score'];
	last_progress = last_record['progress']

	if (last_progress[1] == None and last_progress[3] == None):
		counted[i]    = 's';
	else: 
		counted[i]    = 'lxx';

	if (last_progress[1] != None):
		counted[i-1] = 'l';
		if (last_progress[0] != None):
			counted[i-2] = 'l';
	if (last_progress[3] != None):
		counted[i+1] = 'l';
		i = i+1;
		if (last_progress[4] != None):
			counted[i+1] = 'l';
			i = i+1;
	return i;
		