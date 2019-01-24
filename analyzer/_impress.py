import nltk
import needed.db_mysql as db_mysql

from pprint import pprint;

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

###
 # Count the logic for sentiment
 # @params Integer x, Integer y, String type_logic
 # @return Integer value setiment
def countLogic(x, y, type_logic):
	result = 0;
	if  (x==0): result = y;
	elif(y==0): result = x;
	else:
		if(type_logic == 'AND'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == 'NAND'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = -1;
		elif(type_logic == 'ANDN'):
			if 	 (x==1  and y==1 ):	result = -1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == 'allpo-nepone'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = 1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = 1;
		elif(type_logic == 'allne-nepopo'):
			if 	 (x==1  and y==1 ):	result = -1;
			elif (x==1  and y==-1): result = -1;
			elif (x==-1 and y==1 ):	result = 1;
			elif (x==-1 and y==-1): result = -1;
		elif(type_logic == 'allpo-begpo'):
			if 	 (x==1  and y==1 ):	result = 1;
			elif (x==1  and y==-1): result = 1;
			elif (x==-1 and y==1 ):	result = -1;
			elif (x==-1 and y==-1): result = -1;
	return result;

###
 # Get info type and value sentiment of word
 # @params String word
 # @return Array
def checkSentimentalWord(word):
	result = db_mysql.existSentimentalWord(word);
	if result == None:
		result = [];
		result.append(0);
		result.append(word);
		# result.append(checkWordType(word));
		result.append('unknown');
		result.append(0);
		db_mysql.insertUnknownWord(word);
	
	objWord = db_mysql.existSentimentalWordMainObject(word,'eval');
	result = list(result);
	if (objWord != None):
		result[3] = float(objWord[2]);
	return result;

###
 # Get info type of word from other corpus (kbbi) if there are not in main-corpus
 # @params String word
 # @return Integer type word
def checkWordType(word):
	result = db_mysql.existOtherKamus(word);
	if result == None:
		return 'unknown';
	else:
		return result[2];

###
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

###
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

###
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
		print sentiment;
		valSentiment = valSentiment + sentiment;
	return countingScoreForSentiment(valSentiment);

###
 # Just route for play the role
 # @params Array sentence
 # @return Integer value sentiment
def play(sentence):
	return toRole(sentence);

###
 # The role
 # @params Array sentence
 # @return Integer value sentiment
def toRole(sentence):
	word_token = sentence;
	list_word  = [];
	counted    = [];
	score      = [];

	# get type and val of the words
	jW = 0;
	lenwordtoken = len(word_token) - 1;
	for word in word_token:
		if (word == "di" and jW < lenwordtoken):
			word_next = checkSentimentalWord(word_token[jW+1]);
			if(word_next[2] == W_VERB):
				word_token[jW+1] = "di"+word_token[jW+1];
			jW = jW+1;
			continue;
		result = checkSentimentalWord(word);
		dword  = {'word':word, 'type':result[2], 'value':result[3]};
		list_word.append(dword);
		counted.append('-');
		score.append(0);
		jW = jW+1;

	# pprint(list_word);
	total_word = len(list_word);
	i = 0;

	lstCounting = [];

	while (i < total_word):
		roleGroup = [None] * 5

		#initial word position 
		word_current = list_word[i];
		word_before  = "";
		word_before2 = "";
		word_after   = "";
		word_after2  = "";
		if (i != 0): 			word_before  = list_word[i-1];
		if (i != 0 and i != 1):	word_before2 = list_word[i-2];
		if (i < total_word-1):  word_after   = list_word[i+1];
		if (i < total_word-2):  word_after2  = list_word[i+2]

		iCurrent = i;
		currentPos = checkPositionWord(iCurrent,total_word);

		# Check verb active
		if (word_current['type'] == W_VERB):
			
			counted[iCurrent] = 's';
			score[iCurrent]	= word_current['value'];
			
			if(word_after != "" and (word_after['type'] == W_ADJ or word_after['type'] == W_NOUN)):
				if (word_after['type'] == W_ADJ):
					score[iCurrent] = countLogic(score[iCurrent],word_after['value'],'NAND');
					if(word_after2 != "" and word_after2['type'] == W_NOUN):
						score[iCurrent] = countLogic(score[iCurrent],word_after2['value'],'AND');
						counted[iCurrent+2] = 'l';
						i = i+1;
						roleGroup[4] = word_after2;

				elif (word_after['type'] == W_NOUN):
					score[iCurrent] = countLogic(score[iCurrent],word_after['value'],'AND');
					if(word_after2 != "" and word_after2['type'] == W_ADJ):
						score[iCurrent] = countLogic(score[iCurrent],word_after2['value'],'NAND');
						if(word_current['value'] == -1):
							score[iCurrent] = countLogic(score[iCurrent],word_after2['value'],'allpo-nepone');
						counted[iCurrent+2] = 'l';
						i = i+1;
						roleGroup[4] = word_after2;
					
				counted[iCurrent+1] = 'l';
				counted[iCurrent] 	= 'lxx';
				i = i+1;
				roleGroup[3] = word_after;
				roleGroup[2] = word_current;

			if(word_before != "" and (word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI or word_before['type'] == W_NOUN)):
				if(word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
					scoreBF = score[iCurrent];
					score[iCurrent] = countLogic(word_before['value'], score[iCurrent], 'AND');
					if(word_before2 != "" and word_before2['type'] == W_NOUN):
						if ((word_current['value'] == 1) and (word_after != "" and word_after['value'] == 1)):
							canAccess = 1;
							if(word_after2 != "" and word_after2['value'] != 1):
								canAccess = 0;
							if(canAccess == 1):
								logicNP = countLogic(word_before2['value'], word_before['value'], 'AND');
								score[iCurrent] = countLogic(logicNP, scoreBF, 'AND');
								counted[iCurrent-2] = 'l';
								roleGroup[0] = word_before2;
						if (word_after == "" and word_after2 == ""):
							score[iCurrent] = countLogic(word_before2['value'], score[iCurrent], 'AND');
							counted[iCurrent-2] = 'l';
							roleGroup[0] = word_before2;

				elif(word_before['type'] == W_NOUN):
					scoreBF = score[iCurrent];
					score[iCurrent] = countLogic(word_before['value'], score[iCurrent], 'NAND');
					if ((word_current['value'] == 1) and (word_after != "" and word_after['value'] == 1)):
						canAccess = 1;
						if(word_after2 != "" and word_after2['value'] != 1):
							canAccess = 0;
						if(canAccess == 1):
							score[iCurrent] = countLogic(word_before['value'], scoreBF, 'AND');
							if(word_before2 != ""):
								if(word_before2['type'] == W_ADV or word_before2['type'] == W_PREPOSISI):
									logicNP = countLogic(word_before2['value'], word_before['value'], 'AND');
									score[iCurrent] = countLogic(logicNP, scoreBF, 'AND');
									counted[iCurrent-2] = 'l';
									roleGroup[0] = word_before2;

					else:
						if(word_before2 != "" and (word_before2['type'] == W_ADV or word_before2['type'] == W_PREPOSISI)):
							score[iCurrent] = countLogic(word_before['value'], score[iCurrent], 'AND');

				counted[iCurrent-1] = 'l';
				counted[iCurrent] 	= 'lxx';
				roleGroup[1] = word_before;
				roleGroup[2] = word_current;

		# Check verb passive
		elif (word_current['type'] == W_VERB_DI):

			counted[iCurrent] = 's';
			score[iCurrent]	= word_current['value'];
			
			if(word_before != "" and (word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI or word_before['type'] == W_NOUN)):
				if(word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
					score[iCurrent] = countLogic(word_before['value'], score[iCurrent], 'AND');	
					
					if(word_before2 != "" and word_before2['type'] == W_NOUN):
						score[iCurrent] = countLogic(word_before2['value'], score[iCurrent], 'AND');
						counted[iCurrent-2] = 'l';
						roleGroup[0] = word_before2;

				elif(word_before['type'] == W_NOUN):
					score[iCurrent] = countLogic(word_before['value'], score[iCurrent], 'AND');
					
					if(word_before2 != "" and (word_before2['type'] == W_ADV or word_before2['type'] == W_PREPOSISI)):
						score[iCurrent] = countLogic(word_before2['value'], score[iCurrent], 'AND');
						counted[iCurrent-2] = 'l';
						roleGroup[0] = word_before2;

				counted[iCurrent-1] = 'l';
				counted[iCurrent] 	= 'lxx';
				roleGroup[1] = word_before;
				roleGroup[2] = word_current;


			if(word_after != "" and (word_after['type'] == W_ADJ or word_after['type'] == W_NOUN)):
				scoreCurrent = score[iCurrent];

				if (word_after['type'] == W_ADJ):
					score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'NAND');
					
					if(word_before != ""):
						if(word_before['type'] == W_PREPOSISI or word_before['type'] == W_ADV):
							if(word_before['value'] == -1):
								score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'ANDN');
								if(word_before2 != ""):
									if(word_before2['type'] == W_NOUN):
										if(word_before2['value'] == -1):
											score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'AND');
						
					if(word_after2 != "" and word_after2['type'] == W_NOUN):
						scoreCurrent = score[iCurrent];
						score[iCurrent] = countLogic(scoreCurrent,word_after2['value'],'NAND');

						if(word_before != ""):
							if(word_before['type'] == W_PREPOSISI or word_before['type'] == W_ADV):
								if(word_before['value'] == -1):
									if(word_current['value'] == -1):
										score[iCurrent] = -1;
										if(word_before2 != ""):
											if(word_before2['type'] == W_NOUN):
												if(word_before2['value'] == -1):
													score[iCurrent] = countLogic(scoreCurrent,word_after2['value'],'NAND');
												else:
													score[iCurrent] = -1;
									else:
										score[iCurrent] = countLogic(scoreCurrent,word_after2['value'],'AND');
										if(word_before2 != ""):
											if(word_before2['type'] == W_NOUN):
												if(word_before2['value'] == -1):
													score[iCurrent] = countLogic(scoreCurrent,word_after2['value'],'allpo-begpo');

						counted[iCurrent+2] = 'l';
						i = i+1;
						roleGroup[4] = word_after2;

				if (word_after['type'] == W_NOUN):
					score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'NAND');
					
					if (word_before != ""):
						if(word_before['type'] == W_PREPOSISI or word_before['type'] == W_ADV):
							if(word_before['value'] == -1):
								score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'allpo-nepone');
								if (word_before2 != "" and word_before2['type'] == W_NOUN):
									if(word_before2['value'] == -1):
										score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'NAND');
							else:
								score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'NAND');
								
						elif(word_before['type'] == W_NOUN):
							score[iCurrent] = countLogic(scoreCurrent,word_after['value'],'NAND');

					
					if(word_after2 != "" and word_after2['type'] == W_ADJ):
						score[iCurrent] = countLogic(score[iCurrent],word_after2['value'],'NAND');
						counted[iCurrent+2] = 'l';
						i = i+1;
						roleGroup[4] = word_after2;
					
				counted[iCurrent+1] = 'l';
				counted[iCurrent] 	= 'lxx';
				i = i+1;
				roleGroup[3] = word_after;
				roleGroup[2] = word_current;
		
		# Check adjective
		elif (word_current['type'] == W_ADJ):

			counted[iCurrent] = 's';
			score[iCurrent]	= word_current['value'];
			
			if(word_before != "" and (word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI or word_before['type'] == W_NOUN)):
				scoreCurrent = score[iCurrent];
				
				if(word_before['type'] == W_NOUN):
					score[iCurrent] = countLogic(word_before['value'], scoreCurrent, 'NAND');
				# if(word_before['type'] == W_NOUN and (word_after == "" or (word_after['type']!=W_VERB and word_after['type']!=W_VERB_DI))):
					# score[iCurrent] = countLogic(word_before['value'], scoreCurrent, 'NAND');
					if(word_before2 != "" and (word_before2['type'] == W_ADV or word_before2['type'] == W_PREPOSISI)):
						scoreCurrent = score[iCurrent];
						score[iCurrent] = countLogic(word_before2['value'], scoreCurrent, 'AND');
						counted[iCurrent-2]= 'l';
						roleGroup[0] = word_before2;
				
				elif(word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
					score[iCurrent] = countLogic(word_before['value'], scoreCurrent, 'AND');
					if(word_before2 != "" and word_before2['type'] == W_NOUN):
						scoreCurrent = score[iCurrent];
						score[iCurrent] = countLogic(word_before2['value'], scoreCurrent, 'AND');
						counted[iCurrent-2]= 'l';
						roleGroup[0] = word_before2;

				counted[iCurrent] = 'lxx';
				counted[iCurrent-1]= 'l';
				roleGroup[1] = word_before;
				roleGroup[2] = word_current;

			if(word_after != "" and (word_after['type'] == W_NOUN or word_after['type'] == W_VERB or word_after['type'] == W_VERB_DI)):
				scoreCurrent = score[iCurrent];
				if(word_after['type'] == W_NOUN):
					score[iCurrent] = countLogic(scoreCurrent, word_after['value'], 'AND');

				elif(word_after['type'] == W_VERB or word_after['type'] == W_VERB_DI):
					score[iCurrent] = countLogic(scoreCurrent, word_after['value'], 'NAND');

					if(word_before != ""):
						if(word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
							score[iCurrent] = countLogic(scoreCurrent, word_after['value'], 'AND');
							# scoreCurrent = score[iCurrent];
							# if(word_before2 != "" and word_before2['type'] == W_NOUN):
							# 	score[iCurrent] = countLogic(scoreCurrent, word_after['value'], 'AND');

						elif(word_before['type'] == W_NOUN):
							if(word_before['value'] == -1):
								score[iCurrent] = -1;
							else:
								score[iCurrent] = countLogic(scoreCurrent, word_after['value'], 'NAND');

					if(word_after2 != "" and word_after2['type'] == W_NOUN):
						scoreCurrent = score[iCurrent];
						score[iCurrent] = countLogic(scoreCurrent, word_after2['value'], 'AND');

						if(word_before != "" and word_before['type'] == W_NOUN and word_before['value'] == -1):
							if(word_before2 != "" and (word_before2['type'] == W_PREPOSISI or word_before2['type'] == W_ADV)):
								pass;
							else:
								score[iCurrent] = -1;
						counted[iCurrent+2]= 'l';
						i = i+1;
						roleGroup[4] = word_after2;

				counted[iCurrent+1] = 'l';
				counted[iCurrent] = 'lxx';
				i = i+1;
				roleGroup[3] = word_after;
				roleGroup[2] = word_current;

		elif (word_current['value'] != 0 and (word_current['type'] != W_PREPOSISI and word_current['type'] != W_ADV and word_current['type'] != W_NOUN)):
			score[iCurrent] 	= word_current['value'];
			counted[iCurrent]	= 'ss';

		# Out of counting;
		else:
			counted[iCurrent] = 'x';

		i = i+1;
		if(roleGroup[2] != None):
			lstCounting.append(roleGroup);


	# add role for noun, but after main role done
	# i = 0;
	# while (i < total_word):
	# 	word_current = list_word[i];
	# 	word_before  = "";
	# 	word_before2 = "";
	# 	word_after   = "";
	# 	word_after2  = "";
	# 	if (i != 0): 			word_before  = list_word[i-1];
	# 	if (i != 0 and i != 1):	word_before2 = list_word[i-2];
	# 	if (i < total_word-1):  word_after   = list_word[i+1];
	# 	if (i < total_word-2):  word_after2  = list_word[i+2];
	# 	iCurrent = i;

	# 	if(counted[iCurrent] == "x" and word_current['type'] == W_NOUN):
	# 		if(word_after != "" and counted[iCurrent+1] == "x" and word_after['type'] == W_NOUN):
	# 			score[iCurrent] = countLogic(word_current['value'], word_after['value'], 'NAND');
				
	# 			if(word_after2 != "" and counted[iCurrent+2] == "x" and word_after2['type'] == W_NOUN):
	# 				scoreCurrent = score[iCurrent];
	# 				score[iCurrent] = countLogic(scoreCurrent, word_after2['value'], 'NAND');
	# 				counted[iCurrent+2] = 'ln';
	# 				i = i+1;
				
	# 			counted[iCurrent] = 'lnn';
	# 			counted[iCurrent+1] = 'ln';
	# 			i = i+1;
	# 	i = i+1;

	
	ret = {};
	ret['words']   = list_word;
	ret['score']   = score;
	ret['counted'] = counted;
	ret['roleGroup'] = lstCounting;
	# print score;
	# print counted;
	score = sum(score);
	ret['sentiment'] = countingScoreForSentiment(score);
	return ret;


def toRole2(sentence):
	word_token = sentence;
	list_word = [];
	counted = [];
	score   = [];

	for word in word_token:
		result = checkSentimentalWord(word);
		dword  = {'word':word, 'type':result[2], 'value':result[3]};
		list_word.append(dword);
		counted.append('-');
		score.append(0);

	# pprint(list_word);
	total_word = len(list_word);
	
	i = 0;
	while (i < total_word):
		
		#initial word position :v 
		word_current = list_word[i];
		if (i != 0): 			word_before  = list_word[i-1];
		if (i != total_word-1): word_after   = list_word[i+1];

		# Cek kata verba
		if (word_current['type'] == W_VERB or word_current['type'] == W_VERB_DI):
			if (i != 0 and i != total_word-1): #jika kata ditengah-tengah kalimat
				# Cek ada keterangan sebelum verba
				if (word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
					# print "ada ket sebelum verb";
					# cek ada adj setelah verb
					if (word_after['type'] == W_ADJ):
						verb_adj = countLogic(word_current['value'],word_after['value'],'NAND');
						score[i] = countLogic(word_before['value'], verb_adj, 'AND');
						counted[i-1] = 'l';
						counted[i+1] = 'l';
						i = i+1;
					else:
						score[i] = countLogic(word_before['value'], word_current['value'], 'AND');
					counted[i] 	= 'l';
					counted[i-1]= 'l';
				# Cek ada adj setelah verba
				elif (word_after['type'] == W_ADJ):
					# print "ada adj sesudah verb";
					score[i] 	= countLogic(word_current['value'], word_after['value'], 'NAND');
					counted[i] 	= 'l';
					counted[i+1]= 'l';
					i = i+1;
				else:
					score[i] 	= word_current['value'];
					counted[i] 	= 's';
			elif (i != total_word-1): #jika kata diawal kalimat
				# Cek ada adjektiva sesudah verba
				if (word_after['type'] == W_ADJ):
					score[i]	= countLogic(word_current['value'], word_after['value'], 'NAND');
					counted[i] 	= 'l';
					counted[i+1]= 'l';
					# print word_after['word'] + " -adj setelah verba- " + word_current['word'];
					i = i+1;
				else:
					score[i] 	= word_current['value'];
					counted[i]	= 's';
			else:
				score[i] 	= word_current['value'];
				counted[i] 	= 's';

		# Cek kata adjektiva
		elif (word_current['type'] == W_ADJ):
			# print "ok";
			if (i != 0): # jika tidak di awal kalimat
				# cek ada kata keterangan sebelumnya
				if (word_before['type'] == W_ADV or word_before['type'] == W_PREPOSISI):
					if (word_after['type'] == W_VERB):
						pre_adj 	= countLogic(word_before['value'], word_current['value'], 'NAND');
						score[i]	= countLogic(pre_adj, word_after['value'], 'AND');
						counted[i-1]= 'l';
						counted[i+1]= 'l';
						i = i+1;
					else:
						score[i] = countLogic(word_before['value'], word_current['value'], 'AND');
					counted[i] = 'l';
					counted[i-1] = 'l';
				else:
					score[i] 	= word_current['value'];
					counted[i] 	= 's';
			elif (i != total_word-1): # jika di awal kalimat
				# cek ada kata verb setelahnya
				if (word_after['type'] == W_VERB):
					score[i] 	= countLogic(word_current['value'], word_after['value'], 'NAND');
					counted[i] 	= 'l';
					counted[i+1]= 'l';
					i = i+1;
				else:
					score[i]	= word_current['value'];
					counted[i]	= 's';
			else:
				score[i] 	= word_current['value'];
				counted[i]	= 's';

		elif (word_current['value'] != 0 and (word_current['type'] != W_PREPOSISI or word_current['type'] != W_ADV or word_current['type'] != W_KONJUNGSI or word_current['type'] != W_INTERJEKSI or word_current['type'] != W_NUMERALIA)):
			score[i] 	= word_current['value'];
			counted[i]	= 's';
			# print "lainnya"

		else:
			# print "tidak dihitung";
			counted[i] = 'x';
		
		i = i+1;

	# print score;
	# print counted;
	score = sum(score);
	return countingScoreForSentiment(score);