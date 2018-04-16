# -*- coding: utf-8 -*-


#leidub osalauses esineb kindla morfanalüüsiga sõna
#cm+:_V_ aux  clause_morf+:
#cl+:koer        clause_lemma+:koer


#Supported input format XML-like format as shown below:



#Output format inforem

######## libraries ########
from __future__ import print_function

import os
import re
import sys
import codecs


#############################################
#   common functions
#############################################
def isPythonVersion(version):
	if float(sys.version[:3]) == version:
		return True
	else:
		return False

def make_sure_path_exists(path):
	import errno
	try:
		os.makedirs(path)
	except NameError as exception:
		print('here')
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
		
		
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)



class bColors:
	colors1 = (
		'\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m', '\033[1;37m', '\033[1;38m',
		'\033[1;39m'
	)

	style = {
		'bold': '\033[1m'
		, 'red': '\033[1;31m'
		, 'green': '\033[0;32m'
		, 'yellow': '\033[0;33m'
		, 'blue': '\033[0;34m'
		, 'endc': '\033[0m'
	}
	pattern_red = style['red'] + '%s'   + style['endc']
	pattern_yellow = style['yellow']    + '%s' + style['endc']
	pattern_green = style['green']      + '%s' + style['endc']
	pattern_blue = style['blue']        + '%s' + style['endc']
	pattern_bold = style['bold']        + '%s' + style['endc']

	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


if __name__ == '__main__':
	if sys.stdout.encoding is None:
		eprint(
			bColors.pattern_red % "please set python env PYTHONIOENCODING=UTF-8, example: export PYTHONIOENCODING=UTF-8, when write to stdout.")
		exit(1)
		


def path_leaf(path):
	import ntpath
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)


################################
# dictionary functions and global variables
#############################

######## dictonary functions ########



def read_parse_dict(dictname, dict={}):
	
	global global_conf
	try:
		f_tsv_dict = codecs.open(dictname, "r", "utf-8")
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open %s' % dictname))
		exit()
		
	dict_rows_count=0
	with f_tsv_dict as tsv:
		for line in tsv:
			line = line.strip()
			row = line.split("\t")
			if len(row)>=2:
				if row[1]!='0':
					dict_rows_count += 1
					dict_record={}
					if not row[0].lower() in dict:
						dict[row[0].lower()]=[]
					dict_record['morf'] = row[1]
					dict_record['rules'] = []
					i=2
					while i<len(row):

						#lemma rules
						if row[i][:2] == 'l+':
							dict_record['rules'].append({'ruletype' :'lemma+', 'condition': row[i][2:]})
						
						elif row[i][:2] == 'l-':
							dict_record['rules'].append({'ruletype' :'lemma-','condition' : row[i][2:]})
							
						elif row[i][:3] == 'pl+':
							dict_record['rules'].append({'ruletype' :'prev_lemma+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'pl-':
							dict_record['rules'].append({'ruletype' :'prev_lemma-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'nl+':
							dict_record['rules'].append({'ruletype' :'next_lemma+','condition' : row[i][3:]})
							
						elif row[i][:3] == 'nl-':
							dict_record['rules'].append({'ruletype' :'next_lemma-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'cl+':
							dict_record['rules'].append({'ruletype' :'clause_lemma+','condition' : row[i][3:]})
							
						elif row[i][:3] == 'cl-':
							dict_record['rules'].append({'ruletype' :'clause_lemma-','condition' :  row[i][3:]})
						
						#morfological category rules
						elif row[i][:3] == 'pm+':
							dict_record['rules'].append({'ruletype' :'prev_morf+','condition' : row[i][3:]})
							
						elif row[i][:3] == 'pm-':
							dict_record['rules'].append({'ruletype' :'prev_morf-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'nm+':
							dict_record['rules'].append({'ruletype' :'next_morf+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'nm-':
							dict_record['rules'].append({'ruletype' :'next_morf-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'cm+':
							dict_record['rules'].append({'ruletype' :'clause_morf+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'cm-':
							dict_record['rules'].append({'ruletype' :'clause_morf-','condition' :  row[i][3:]})
						
						#grammatical category rules
						elif row[i][:2] == 'g+':
							dict_record['rules'].append({'ruletype' :'gramcat+','condition' :  row[i][2:]})
							
						elif row[i][:2] == 'g-':
							dict_record['rules'].append({'ruletype' :'gramcat-','condition' :  row[i][2:]})
							
						elif row[i][:3] == 'pg+':
							dict_record['rules'].append({'ruletype' :'prev_gramcat+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'pg-':
							dict_record['rules'].append({'ruletype' :'prev_gramcat-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'ng+':
							dict_record['rules'].append({'ruletype' :'next_gramcat+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'ng-':
							dict_record['rules'].append({'ruletype' :'next_gramcat-','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'cg+':
							dict_record['rules'].append({'ruletype' :'clause_gramcat+','condition' :  row[i][3:]})
							
						elif row[i][:3] == 'cg-':
							dict_record['rules'].append({'ruletype' :'clause_gramcat-','condition' :  row[i][3:]})
	
						i+=1
					dict[row[0].lower()].append( dict_record)
			

	if 'v' in global_conf['conf']['verbose']:
		eprint('Imported %d rules from %s' % (dict_rows_count, dictname))

	return dict

##########################################
# sentence dict functions
##########################################


def transform_with_weight(sentence_dict, dict):
	global missing_morf
	global global_conf
	dict_weight = global_conf['dict_weight']
	
	
	#lisame siia ühe tsükli, et säilitada lause originaalsed morf_märgendid osalause reeglite kontrollimiseks
	
	for lineid in sorted(sentence_dict['lines']):
		if sentence_dict['lines'][lineid]['type'] == 'token':
			sentence_dict['lines'][lineid]['info']['analys']['prev_morf'] = []
			for morf in sentence_dict['lines'][lineid]['info']['analys']['morf']:
				sentence_dict['lines'][lineid]['info']['analys']['prev_morf'].append(morf)
	
	
	SEPARATOR = '|'
	#translation part
	for lineid in sorted(sentence_dict['lines']):
		
		if sentence_dict['lines'][lineid]['type'] == 'token':
			
			for i,v in enumerate(sentence_dict['lines'][lineid]['info']['analys']['lemma']):
				lemma = v
				morf_orig    = sentence_dict['lines'][lineid]['info']['analys']['prev_morf'][i]
				morf         = sentence_dict['lines'][lineid]['info']['analys']['morf'][i]
				# kui   leidusid reeglid sellisele morf infole
				# siis käime kõik reeglid läbi ning salvestame koos kaaluga massiivi
				# lõpus valime suurima kaaluga matchi
				
				#kui reegli mingi osa ei matchinud, siis järgnevaid osasid enam ei kontrollita ja skoor nullitakse
				matched_rules={}
				if morf.lower() in dict:
					#print(dict[morf.lower()])
					#rules = dict[morf.lower()]['rules']
								
					for dictrow in dict[morf.lower()]:
						rulemorf = dictrow['morf']
						rule_total_weight = 1
						rules = dictrow['rules']
						for rule in rules:
							ruletype = rule['ruletype']
						
							if rule_total_weight == 0:
								break
							sub_weigth = 0
							
							rule_strings = rule['condition'].lower().split(SEPARATOR)
							#eprint(rule_strings)
							strings_to_compare = []
							
			
							if ruletype in ['lemma+', 'lemma-']:
								strings_to_compare = [lemma]
							
							elif ruletype in ['gramcat+', 'gramcat-']:
								strings_to_compare = [morf_orig]
							
							elif ruletype in ['prev_lemma+', 'prev_lemma-', 'prev_morf+', 'prev_morf-' ,'prev_gramcat+', 'prev_gramcat-']:
								if lineid == 1 or sentence_dict['lines'][lineid-1]['type'] != 'token':
									if ruletype[-1:] == '-':
										rule_total_weight += dict_weight[ruletype]
									else:
										rule_total_weight = 0
									continue
								
								if ruletype in ['prev_lemma+', 'prev_lemma-']:
									strings_to_compare = sentence_dict['lines'][lineid-1]['info']['analys']['lemma']
								elif ruletype in ['prev_morf+', 'prev_morf-', 'prev_gramcat+', 'prev_gramcat-']:
									strings_to_compare = sentence_dict['lines'][lineid-1]['info']['analys']['prev_morf']
									
									
							elif ruletype in ['next_lemma+', 'next_lemma-', 'next_morf+', 'next_morf-', 'next_gramcat+', 'next_gramcat-' ]:
								if lineid == len(sentence_dict['lines']) or sentence_dict['lines'][lineid+1]['type'] != 'token':
									if ruletype[-1:] == '-':
										rule_total_weight += dict_weight[ruletype]
									else:
										rule_total_weight = 0
									continue
								if ruletype in ['next_lemma+', 'next_lemma-']:
									strings_to_compare = sentence_dict['lines'][lineid+1]['info']['analys']['lemma']
								elif ruletype in ['next_morf+', 'next_morf-', 'next_gramcat+', 'next_gramcat-']:
									strings_to_compare = sentence_dict['lines'][lineid+1]['info']['analys']['prev_morf']
									
									
									
							elif ruletype in ['clause_lemma+', 'clause_lemma-', 'clause_morf+', 'clause_morf-', 'clause_gramcat+', 'clause_gramcat-' ]:
								clause_id = sentence_dict['lines'][lineid]['clause_id']
								#kui osalauses ainult yks liige
								if len(g_d_sentence['clauseTokens'][clause_id]) == 1:
									if ruletype[-1:] == '+':
										rule_total_weight = 0
									else:
										rule_total_weight += dict_weight[ruletype]
									continue
									
									
									
								if ruletype in ['clause_lemma+', 'clause_lemma-']:
									for id in g_d_sentence['clauseTokens'][clause_id]:
										if id != lineid:
											lemmas_array = sentence_dict['lines'][id]['info']['analys']['lemma']
											for c_lemma in lemmas_array:
												strings_to_compare.append(c_lemma)
								
								elif ruletype in ['clause_morf+', 'clause_morf-', 'clause_gramcat+', 'clause_gramcat-']:
									for id in g_d_sentence['clauseTokens'][clause_id]:
										if id != lineid:
											morf_array = sentence_dict['lines'][id]['info']['analys']['prev_morf']
											for c_morf in morf_array:
												strings_to_compare.append(c_morf)

							###########
							#eprint (strings_to_compare)

							#gramcat rules
							if ruletype[-9:] == '_gramcat+':
								sub_weigth = 0
								for text_string in strings_to_compare:
									array_gramcats = text_string.lower().split(' ')
									sub_sub_weigth = 0
									
									if set(rule_strings) < set(array_gramcats):
										sub_sub_weigth = dict_weight[ruletype]
									
									if sub_sub_weigth > 0:
										sub_weigth = sub_sub_weigth
										continue
											
								if sub_weigth == 0:
									rule_total_weight = 0
									continue
								rule_total_weight += sub_weigth
								
							elif ruletype[-9:] == '_gramcat-':
								sub_weigth = dict_weight[ruletype]
								#eprint('rule',rule_strings)
								#eprint ('text',strings_to_compare)
								for text_string in strings_to_compare:
									array_gramcats = text_string.lower().split(' ')
									
									if  set(rule_strings) < set(array_gramcats):
										sub_weigth = 0
											
									if sub_weigth == 0:
										rule_total_weight = 0
										continue
								rule_total_weight += sub_weigth
								

							#morf and lemma rules
							elif ruletype[-1:] == '+': #reegel, et string leidub
								sub_weigth = 0
								for text_string in strings_to_compare:
									for rule_string in rule_strings:
										if text_string == rule_string:
											sub_weigth = dict_weight[ruletype]
											#print ('leidus')
											break
								if sub_weigth == 0:
									rule_total_weight = 0
									continue
								rule_total_weight += sub_weigth
							
							elif ruletype[-1:] == '-':
								sub_weigth = dict_weight[ruletype]
								for text_string in strings_to_compare:
									for rule_string in rule_strings:
										if text_string == rule_string:
											sub_weigth = 0
											break
								if sub_weigth == 0:
									rule_total_weight = 0
									continue
								rule_total_weight += sub_weigth
								

						if rule_total_weight > 0:
							matched_rules[rule_total_weight] = rulemorf


				#print (matched_rules)
				#print (morf)
				#kui üksi reegel ei sobinud
				
				if not matched_rules:
					missing_morf[morf_orig] = 1

				else:
					sentence_dict['lines'][lineid]['info']['analys']['morf'][i] = matched_rules[(max(matched_rules.keys(), key=int))]
	


	return sentence_dict


######################################
#   inforem output functions
####################################

def construct_inforem_sentence(sentence, sentence_id):
	global global_conf
	flags = global_conf['conf']['flags']
	sentence_str = ''
	if not '1' in flags:
		sentence_str = "\"<s id=\"%d\">\"\n\n" % sentence_id
	for line_id in sorted(sentence['lines']):
		if g_d_sentence['lines'][line_id]['type'] == 'token':
			sentence_str += construct_line_inforem(sentence['lines'][line_id]['info']) + "\n"
	if not '1' in flags:
		sentence_str += '"</s>"' + "\n" + "\n"
	return sentence_str


def construct_line_inforem(dict_info):


	return_line_pattern = '"<%s>"%s'
	morf_pattern1 = "\n\t" + '"%s" L%s %s%s%s%s%s%s'
	morf_pattern2 = "\n\t" + '"%s" %s %s%s%s%s%s'
	function_pattern = ' %s'
	relation_pattern = ' #%s'

	pattern_synt_rel = ' {%s:%s}'

	pattern_synt_type = ' {%s}'
	pattern_pos = '%s '
	synt_relations = ''
	if 'ann_relations' in dict_info:
		# synt_relations =   dict_info['ann_relations']
		for rel in dict_info['ann_relations']:
			synt_relations += (pattern_synt_rel % (rel, ','.join(dict_info['ann_relations'][rel])))

	synt_type = ''
	if 'ann_type' in dict_info:
		synt_type = pattern_synt_type % dict_info['ann_type']
	str_morf = ''

	for i, v in enumerate(dict_info['analys']['lemma']):
		lemma = v
		morf = dict_info['analys']['morf'][i]
		case = dict_info['analys']['case'][i]
		pos = dict_info['analys']['pos'][i]
		functions = ''
		relations = ''

		if dict_info['analys']['function'][i] != '':
			functions = function_pattern % (dict_info['analys']['function'][i])
		if dict_info['analys']['relation'][i] != '':
			relations = relation_pattern % (dict_info['analys']['relation'][i])
		if pos:
			pos = pattern_pos % pos
		if case != '':
			str_morf = str_morf + (morf_pattern1 % (lemma, case, pos, morf, functions, relations, synt_type, synt_relations))
		else:
			str_morf = str_morf + (morf_pattern2 % (lemma, pos, morf, functions, relations, synt_type, synt_relations))
		str_morf = str_morf.replace('  ',' ')

	return return_line_pattern % (dict_info['token'], str_morf)


##################################
#   estmorf input parse functions
#################################

def new_clause_id():
	"""

	:rtype: int
	"""
	global g_d_sentence
	if 'clauseTokens' in g_d_sentence:
		newKey = max(g_d_sentence['clauseTokens'].keys()) + 1
		g_d_sentence['clauseTokens'][newKey] = []

		return newKey
	else:
		g_d_sentence['clauseTokens'] = {}
		g_d_sentence['clauseParent'] = {}
		g_d_sentence['clauseTokens'][1] = []
		g_d_sentence['clauseParent'][1] = 0
		return 1

def parseTokenLineToDict(line):
	#siia lisada range stringi formaadi check ja vastav info stdERRORisse
	#Seoses    Seos+s //_H_ Sg Ine, //    Seose+s //_H_ Sg Ine, //    Seoses+0 //_H_ Sg Nom, //    seos+s //_S_ Sg Ine, //    seoses+0 //_K_ //
	global g_input_line_nr
	dict={}
	errors = []
	line=line.strip()
	#ignore empty lines
	#print (line)
	if line != '':
		result = re.match('(^[^\s+]+)', line)
		dict['token'] = result.group(0)
		result = re.split('\s//\s*', line)
		#print (result);
		if len(result)>1:
			result2 =re.split('\s+', result[0])
			if len(result2)==2:
				#print (result2)
				dict['token'] = result2[0].strip()
				str = result2[1].strip()

				dict['analys']={}
				dict['analys']['lemma']=[]
				dict['analys']['case']=[]
				dict['analys']['morf']=[]
				dict['analys']['pos']=[]
				dict['analys']['function']=[]
				dict['analys']['relation']=[]


				result = re.findall('\s\s\s\s.+\s\/\/.+\/\/', line)
				if len(result) < 1:
					errors.append((bColors.pattern_red % ('\tUnrecognized format on line %d: ' % g_input_line_nr)) + line)
				#print (result
				for i,v in enumerate(result):
					res = re.split(' //', v)
					dict['analys']['pos'].append('')
					lemmacase = re.split('\+', res[0].strip())
					#  print (lemmacase)
					dict['analys']['lemma'].append(lemmacase[0].strip())
					if (len(lemmacase)>1):
						dict['analys']['case'].append(lemmacase[1].strip())
					else:
						dict['analys']['case'].append('')
					dict['analys']['morf'].append(res[1].strip().replace(',',''))
					dict['analys']['function'].append('')
					dict['analys']['relation'].append('')

			else:
				dict['analys'] = {}
				dict['analys']['lemma'] = []
				dict['analys']['case'] = []
				dict['analys']['morf'] = []
				dict['analys']['pos'] = []
				dict['analys']['function'] = []
				dict['analys']['relation'] = []
				dict['analys']['function'].append('')
				dict['analys']['relation'].append('')
				dict['analys']['pos'].append('')
				dict['analys']['lemma'].append('ERROR!!! '+line)
				dict['analys']['case'].append('')
				dict['analys']['morf'].append(line)
				errors.append((bColors.pattern_red % ('\tUnrecognized format on line %d: ' % g_input_line_nr)) + line)


		else:
			dict['analys'] = {}
			dict['analys']['lemma'] = []
			dict['analys']['case'] = []
			dict['analys']['morf'] = []
			dict['analys']['pos'] = []
			dict['analys']['function'] = []
			dict['analys']['relation'] = []
			dict['analys']['lemma'].append('ERROR!!! '+line)
			dict['analys']['case'].append('')
			dict['analys']['function'].append('')
			dict['analys']['relation'].append('')
			dict['analys']['pos'].append('')
			dict['analys']['morf'].append(line)
			errors.append((bColors.pattern_red % ('\tUnrecognized format on line %d: ' % g_input_line_nr)) + line)
	if len(errors):
		eprint()
	for error in errors:
		eprint (bColors.pattern_red % ('\t%s'%error))
		#pp.pprint(dict)

	return (dict)

def makeDictFromArray(aSentence, i=None):
	# sentence_dict['lines'][lineid]['type'] == 'token'
	# dict['analys']={}
	#           dict['analys']['lemma']=[]
	#          dict['analys']['case']=[]
	#         dict['analys']['morf']=[]
	#        dict['analys']['lemma'].append('ERROR!!! '+line)
	#        dict['analys']['case'].append('')
	#        dict['analys']['morf'].append(line)

	#<s>
	#Õigupoolest    õigu_poolest+0 //_D_ //
	#tuli    tule+i //_V_ Pers Prt Ind Sg3 Aff, //
	#kell    kell+0 //_S_ Sg Nom, //
	#12:08    12:08+0 //_N_ ?, //
	#ka    ka+0 //_D_ //
	#teade    teade+0 //_S_ Sg Nom, //
	#,    , //_Z_ //
	#<kindel_piir/>
	#et    et+0 //_J_ //
	#m-parkimine    m-parkimine+0 //_S_ Sg Nom, //
	#ei    ei+0 //_V_ Neg, //
	#toimi    toimi+0 //_V_ Pers Prs Ind Neg, //
	#...    ... //_Z_ //
	#<kindel_piir/>
	#aga    aga+0 //_J_ //
	#selleks    see+ks //_P_ Sg Tra, //
	#ajaks    aeg+ks //_S_ Sg Tra, //
	#teadsin    tead+sin //_V_ Pers Prt Ind Sg1 Aff, //
	#ma    mina+0 //_P_ Sg Nom, //
	#seda    see+da //_P_ Sg Par, //
	#isegi    isegi+0 //_D_ //
	#.    . //_Z_ //
	#</s>

	global g_d_sentence
	global g_input_line_nr


	g_d_sentence = {'lines':{}}
	line_id = 0
	#g_token_id = 0

	level = 1


	clause_id = new_clause_id()

	parent_clause = g_d_sentence['clauseParent'][clause_id]
	#g_d_sentence['clauseParent'][g_clause_id] = parent_clause


	tag_line_pattern = '^<(.+)>$'

	#token_line_pattern = '^(.+)\s\s\s\s((.+) //(.+) //\s*)+$'
	line_id = 0

	for s in aSentence:

		# print (s)
		line_id += 1
		match_tag = re.match(tag_line_pattern, s)
		#match_tokenline = re.match(token_line_pattern, s)

		if match_tag:

			#print (match_tag.groups())
			tag = s
			if match_tag.group(1) == 'kindel_piir/':
				#parent sama
				#clause uus
				clause_id = new_clause_id()
				g_d_sentence['clauseParent'][clause_id] = parent_clause
				g_d_sentence['lines'][line_id] = { 'type':'tag', 'line_id':line_id, 'tag': tag, 'level' : level}

			elif match_tag.group(1) == 'kiil':
				#parent eelmine clause
				#clause uus
				parent_clause = clause_id
				clause_id = new_clause_id()
				g_d_sentence['clauseParent'][clause_id] = parent_clause
				level += 1
				g_d_sentence['lines'][line_id] = { 'type':'tag', 'line_id':line_id, 'tag': tag, 'level' : level}


			elif match_tag.group(1) == '/kiil':
				# parentclause parent
				# clause eelmine clause
				g_d_sentence['lines'][line_id] = { 'type':'tag', 'line_id':line_id, 'tag': tag, 'level' : level}
				level -= 1
				clause_id = g_d_sentence['clauseParent'][clause_id]
				parent_clause = g_d_sentence['clauseParent'][clause_id]

			#print (clause_id, parent_clause, '-'*4*g_d_sentence['lines'][line_id]['level'], s)

		else:
			#print (clause_id, parent_clause, '-'*4*level, s)

			info = parseTokenLineToDict(s)
			g_d_sentence['lines'][line_id] = { 'type':'token', 'line_id':line_id, 'token': s, 'clause_id':clause_id, 'level' : level, 'info':info}
			g_d_sentence['clauseTokens'][clause_id].append(line_id)
			#print (info)

	
def translate(f_input, f_out):
	#global variables
	global g_d_sentence
	global g_input_line_nr
	global missing_morf
	global global_conf
	flags = global_conf['conf']['flags']

	tag_line_pattern = '^.?<.*>$'
	missing_morf = {}
	i = 0
	g_input_line_nr = 0
	arr_sentence = []
	in_sentence = False
	eprint()
	with f_input as fp:
		for line in fp:
			g_input_line_nr += 1
			line = line.strip()
			if line == '':
				continue
			elif '1' in flags:
				
				match_tag = re.match(tag_line_pattern, line)
				if not match_tag:
					arr_sentence = []
					arr_sentence.append(line)
					makeDictFromArray(arr_sentence, i)
					#sys.stderr.write('%d..' % g_input_line_nr)
					#sys.stderr.flush()
					sentence = transform_with_weight(g_d_sentence, dict)
					f_out.write(construct_inforem_sentence(g_d_sentence, i))
					arr_sentence = []

			elif line == '<s>' and in_sentence == False:
				i += 1
				in_sentence = True
	
			elif line == '</s>' and in_sentence == True:
	
				in_sentence = False
				sys.stderr.write('%d..' % i)
				sys.stderr.flush()
	
				makeDictFromArray(arr_sentence, i)
	
				#print (arr_sentence)
				arr_sentence = []
	
				sentence = transform_with_weight(g_d_sentence, dict)
				f_out.write(construct_inforem_sentence(g_d_sentence, i))
	
	
			elif in_sentence:
				#print (line)
				arr_sentence.append(line)
	if missing_morf:
		eprint()
		eprint  (bColors.pattern_blue % '\tMissing morf tags:')
	for morf in sorted(missing_morf):
		eprint (bColors.pattern_blue % ('\t\t%s'%morf))
	
	return 1


def read_local_conf(conffilename):
	global global_conf
	try:
		f_tsv_conf = codecs.open(conffilename, "r", "utf-8")
		if 'v' in global_conf['conf']['verbose']:
			eprint(bColors.pattern_bold % ('Reading conf from %s' % conffilename))
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open %s' % conffilename))
		return 0
		
	dict_rows_count=0
	with f_tsv_conf as tsv:
		for line in tsv:
			line = line.strip()
			row = line.split("\t")
	

			if row[0][:1]=='#':
				continue
			elif row[0][:1]=='':
				continue
			else:
				params = row[0].split('.')
				if params[0] == 'dict_weight' and len(params)==2 and len(row)>1:
					value = row[1].strip()
					if params[1] in global_conf['dict_weight']:
						try:
							global_conf['dict_weight'][params[1]]	= int(value)
						except ValueError:
							eprint(bColors.pattern_red % ('\tInvalid \'dict_weight value\' for \'%s\' in configuration file. \'%s\' should be int.'%(params[1], value)))
							
				elif params[0] == 'conf' and len(params)==2 and len(row)>1:
					value = row[1].strip()
					if params[1] == 'output_extension' and len(value):
						 global_conf['conf']['output_extension']	= value
					elif params[1] == 'output_folder'  and len(value):
						global_conf['conf']['output_folder']	    = value
					elif params[1] == 'default_dictionary'  and len(value):
						global_conf['conf']['default_dictionary']	    = value
					elif params[1] == 'additional_dictionary'  and len(value):
						global_conf['conf']['additional_dictionary']	    = value
	return 1

##################################
#
#################################
import getopt
def usage():
	
	print ("Usage ....")

def main():

	options = {}
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h1c:d:a:f:e:", ["help", "1_line_mode", "dictionary=", "dictionary_additional="])
		
		#print (opts)
	except getopt.GetoptError as err:
		# print help information and exit:
		eprint ("option is not recognized")
		usage()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-c"):
			options['local_conf'] = a
		elif o in ("-d"):
			options['default_dictionary'] = a
		elif o in ("-a"):
			options['additional_dictionary'] = a
		elif o in ("-f"):
			options['output_folder'] = a
		elif o in ("-e"):
			options['output_extension'] = a
		elif o in ("-1"):
			options['1'] = '1'
			
			
			
		else:
			assert False, ("unhandled option %s"%o)
	
	input_files = args
	options['input_files'] = input_files
	return options
	


################################
#       START
##############################



#parsing dictionary
		
script_name = (os.path.realpath(__file__))
script_dir = os.path.dirname(script_name)






global_conf = {}


#DEfault values
global_conf['dict_weight'] = {
	'lemma+'            : 100
	, 'lemma-'          : 100
	, 'prev_lemma+'     : 70
	, 'prev_lemma-'     : 70
	, 'next_lemma+'     : 70
	, 'next_lemma-'     : 70
	, 'clause_lemma+'   : 50
	, 'clause_lemma-'   : 50
	
	, 'prev_morf+'      : 65
	, 'prev_morf-'      : 65
	, 'next_morf+'      : 65
	, 'next_morf-'      : 65
	, 'clause_morf+'    : 50
	, 'clause_morf-'    : 50

	, 'gramcat+'          : 25
	, 'gramcat-'          : 25
	, 'prev_gramcat+'     : 24
	, 'prev_gramcat-'     : 24
	, 'next_gramcat+'     : 24
	, 'next_gramcat-'     : 24
	, 'clause_gramcat+'     : 20
	, 'clause_gramcat-'     : 20
	
	
	}




global_conf['conf'] = {}

global_conf['conf']['output_extension'] = 'mrf.inforem'
global_conf['conf']['output_folder'] = '.'

global_conf['conf']['default_dictionary'] = script_dir+'/dictionaries/giella2cg.tab'
global_conf['conf']['default_conffile'] = script_dir + '/conf/conf.tab'
global_conf['conf']['verbose'] = 'v'
global_conf['conf']['flags'] = ''

commandline_options = {}

if __name__ == "__main__":
	commandline_options = main()

flags = ''



if 'local_conf' in commandline_options:
	global_conf['conf']['default_conffile'] = commandline_options['local_conf']
	




if '1' in commandline_options:
	global_conf['conf']['flags'] += '1'
	#ei lobise nii palju
	global_conf['conf']['verbose'] = ''
#override conf with conffile
read_local_conf(global_conf['conf']['default_conffile'])

if 'output_folder' in commandline_options:
	global_conf['conf']['output_folder'] = commandline_options['output_folder']

make_sure_path_exists(global_conf['conf']['output_folder'])


if 'output_extension' in commandline_options:
	global_conf['conf']['output_extension'] = commandline_options['output_extension']


if 'default_dictionary' in commandline_options:
	global_conf['conf']['default_dictionary'] = commandline_options['default_dictionary']


#additional dictionary
if 'additional_dictionary' in commandline_options:
	global_conf['conf']['additional_dictionary'] = commandline_options['additional_dictionary']
	

if '1' in commandline_options and 'v' in global_conf['conf']['verbose']:
		eprint('\t%s\t%s' % ('1-line mode', 'activated'))
		
		
inputfiles = commandline_options['input_files']



if 'v' in global_conf['conf']['verbose']:
	eprint()
	eprint(bColors.pattern_bold % 'morf2morf.py is running with the following params:')
	eprint('\t%s\t\t%s' % ('local_conffile', global_conf['conf']['default_conffile']))
	eprint('\t%s\t\t%s' % ('output_folder', global_conf['conf']['output_folder']))
	eprint('\t%s\t\t%s' % ('output_extension', global_conf['conf']['output_extension']))
	eprint('\t%s\t\t%s' % ('default_dictionary', global_conf['conf']['default_dictionary']))
	if 'additional_dictionary' in global_conf['conf']:
		eprint('\t%s\t\t%s' % ('additional_dictionary', global_conf['conf']['additional_dictionary']))
	if len(inputfiles):
		eprint('\t%s' % 'Input files:')
		for ifile in inputfiles:
			eprint('\t\t%s' % ifile)
	eprint()



#parsing dictionary
dict = read_parse_dict(global_conf['conf']['default_dictionary'])

#additional dictionary
if 'additional_dictionary' in global_conf['conf']:
	dict = read_parse_dict(global_conf['conf']['additional_dictionary'], dict)


#global variables
global g_d_sentence
global g_input_line_nr
global missing_morf


for input in inputfiles:
	try:
		f_input = codecs.open(input, "r", "utf-8")
		output = global_conf['conf']['output_folder'] +'/' + path_leaf(input) + '.' + global_conf['conf']['output_extension']
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open ' + input))
		continue
	eprint()
	eprint(bColors.pattern_bold %   ("%s -----> %s" % (input, output)))
	# open output file
	try:
		f_out = codecs.open(output, "w", "utf-8")
		
	
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open ' + output))
		continue
		
	translate(f_input, f_out)

	f_out.close()
	f_input.close()
	
if not len(inputfiles) :
	if isPythonVersion(2.7):
		reload(sys)
		sys.setdefaultencoding('utf-8')
	translate(sys.stdin, sys.stdout)


	
eprint()
exit()
