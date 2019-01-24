import helper.preprocessing as preprocessing
import analyzer.impress as impress
import json
from pprint import pprint

# theText = text.main();

# descTheRule = [];

# for text in theText:
# 	keyword = preprocessing.do(text);
# 	result  = impress.play(keyword);

#  	# print text;
#  	# print result['words'];
#  	# print result['sentiment'];
#  	desc = {'text':text,'arr_word':result['words'],'sentiment':result['sentiment'],'recordRuleWork':result['recordRuleWork']};
#  	descTheRule.append(desc);

# with open('testing/jsonDescTheRule.txt', 'w') as outfile:
#     json.dump(descTheRule, outfile)

with open('testing/desc_rule/1RuleCombination.json') as json_data:
    rule_combination = json.load(json_data)

for sub_part in rule_combination:
	for list_combination in rule_combination[sub_part]:
		desc_rule = [];
		name_file = list_combination.replace(' ','');
		
		for example_text in rule_combination[sub_part][list_combination]:
			keyword = preprocessing.do(example_text);
			result  = impress.play(keyword,'eval');
		 	desc    = {'text':example_text,'arr_word':result['words'],'sentiment':result['sentiment'],'recordRuleWork':result['recordRuleWork']};
		 	desc_rule.append(desc);

		with open('testing/desc_rule/'+name_file+'.json', 'w') as outfile:
			json.dump(desc_rule, outfile)
