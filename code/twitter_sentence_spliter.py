#!/usr/bin/python

################################################################################################
# twitter_sentence_spliter.py
# Script for sentence spliting for Twitter
#
# Author: Wei Xu 
#
# @phdthesis{xu2014data,
#  author = {Xu, Wei},
#  title = {Data-Drive Approaches for Paraphrasing Across Language Variations},
# school = {Department of Computer Science, New York University},
# year = {2014}
# }
################################################################################################



from __future__ import division

import re
import string
import HTMLParser
from twokenize import tokenize


# a cleaner verson of sentence spliter, which also get rid of very short sentences etc but only keep meaningful sentences
def splitCleanTweet2Sents(tweet):
	cleansents = []
	rawsents = splitTweet2Sents(tweet)
	for rawsent in rawsents:
		cleansent = cleanSent(rawsent)
		if cleansent != None:
			cleansents.append(cleansent)
	return cleansents

# the entrance of sentence spliter, given a tweet
def splitTweet2Sents(tweet):
	tweet = re.sub(u'\u201c', '\"', tweet)
	tweet = re.sub(u'\u201d', '\"', tweet)
	tweet = tweet.encode('ascii', 'ignore')
	tokenizedtweet = u" ".join(tokenize(tweet))
	cleantweet = filterTweetText(tokenizedtweet)
	sents = sentSplitter(cleantweet)
	return sents

def filterUniqSentSet (sentences) :
	filteredsents = []

	regex = re.compile('[%s]' % re.escape(string.punctuation))
	# replace #hashtag and @usrname
	# merge those are the same
	for sentence in sentences :     
		merged = False
		
		if len(filteredsents) > 0 :
			for i, filteredsent in enumerate(filteredsents) :
                                sentence_nopunc = re.sub(r' +', r' ', regex.sub('', sentence)).strip()
                                filteredsent_nopunc = re.sub(r' +', r' ', regex.sub('', filteredsent)).strip()
				# print sentence_nopunc
				# print filteredsent_nopunc
				# print
				if sentence.lower() in filteredsent.lower() or sentence_nopunc.lower() in filteredsent_nopunc.lower():
					merged = True
					break
				if filteredsent.lower() in sentence.lower() or filteredsent_nopunc.lower() in sentence_nopunc.lower():
					filteredsents[i] = sentence
					merged = True
					break
							
		if merged == False :
			filteredsents.append(sentence.strip())

	dsent_count = {}
	dsent_sent = {}
	
	for sentence in filteredsents :
		dsentence = re.sub(r'[@#]\S+', r'', sentence)	
		dsentence = re.sub(r' +', r'', dsentence)	
		dsentence = re.sub(r'\d+', r'%NUMBER%', dsentence)
		dsent_count[dsentence] = dsent_count.get(dsentence, 0.0) + 1.0
		if dsentence in dsent_sent:
			if len(sentence) < len(dsent_sent[dsentence]) :
				dsent_sent[dsentence] = sentence
		else :
			dsent_sent[dsentence] = sentence
	
	filteredsents2 = []
	
	for sentence in filteredsents :
		dsentence = re.sub(r'[@#]\S+', r'', sentence)	
		dsentence = re.sub(r' +', r'', dsentence)
		dsentence = re.sub(r'\d+', r'%NUMBER%', dsentence)	
		if dsent_count[dsentence] == 1 :
			filteredsents2.append(sentence)
		else :
			filteredsents2.append(dsent_sent[dsentence])
	
	filteredsents2 = list(set(filteredsents2))
	
	return filteredsents2

# Remove symbols, emticons, urls from tweet
def filterTweetText (tokenizedtext) :

	tokenizedtext = re.sub(r'& quot ;', r'&quot;' , tokenizedtext)

	tokenizedtext = HTMLParser.HTMLParser().unescape(tokenizedtext.strip())
	
	
		
	tokenizedtext = re.compile(r'\(.*via.*\)', re.IGNORECASE).sub(r'|', tokenizedtext)
	tokenizedtext = re.compile(r'rt @\S+', re.IGNORECASE).sub(r'|', tokenizedtext)
	tokenizedtext = re.compile(r'http[^\s]+', re.IGNORECASE).sub(r'|', tokenizedtext)
	#tokenizedtext = re.compile(r'rt [^\s]+ :', re.IGNORECASE).sub(r'|', tokenizedtext)
	tokenizedtext = re.compile(r'via @\S+', re.IGNORECASE).sub(r'|', tokenizedtext)
	tokenizedtext = re.sub(r'\(.*\)', r'', tokenizedtext)
	tokenizedtext = re.sub(r'\[.*\]', r'', tokenizedtext)
	tokenizedtext = re.sub(r'\/.*\/', r'', tokenizedtext)
	tokenizedtext = re.sub(r'\.\.+', r'.', tokenizedtext)
	tokenizedtext = re.sub(r'!!+', r'!', tokenizedtext)
	tokenizedtext = re.sub(r'\|\|+', r'|', tokenizedtext)
	tokenizedtext = re.sub(r'\?\?+', r'?', tokenizedtext)
	tokenizedtext = re.sub(r'--+', r'--', tokenizedtext)
	tokenizedtext = re.sub(r'< 3', r'<3', tokenizedtext)

	tokens = tokenizedtext.split()
	
	puretokens = []
	atthebegin = True
	for i in xrange(0, len(tokens)) :
		curtoken = tokens[i]
		nexttoken = ''
		if i < len(tokens) - 1 :
			nexttoken = tokens[i+1]
		nexttokenflag = False
		if nexttoken == '\'s' or nexttoken == 'is' or nexttoken == 'are' or nexttoken == 'will' or nexttoken == 'has' or nexttoken == 'have' or nexttoken == '\'re' or nexttoken == 'was' or nexttoken == 'were' :
			nexttokenflag = True			
	
		if curtoken[0] == ':' and atthebegin == True:
			continue
		if curtoken[0] == '@' and atthebegin == True and nexttokenflag == False:
			continue
		if curtoken[0] == '#' and atthebegin == True and nexttokenflag == False:
			continue
		if re.match(r'retweet$', curtoken, re.IGNORECASE) and atthebegin == True:
			continue   
		if re.match(r'rt$', curtoken, re.IGNORECASE) and atthebegin == True:
			continue   

		atthebegin = False
		puretokens.append(curtoken)
	
	
	text = ' '.join(puretokens)  
       
	return text  
	
# main sentence spliter	for tweets
def sentSplitter (cleantext) :
		
	tokens = cleantext.split()
	
	sents = []
	
	senttokens = []
	count = 0
	
	countquote = cleantext.count('\"')
	
	for i, curtoken in enumerate(tokens) :

		if curtoken[len(curtoken)-1] != '\"' or (countquote > 1 and cleantext[0] != '\"') :
			senttokens.append(curtoken)
		
		if curtoken == '-' or curtoken == '.' or curtoken == ':' or curtoken == '~' or curtoken == '|'  or curtoken == '!' or curtoken == '!' or curtoken == '?' or re.search(r'<', curtoken) or re.search(r'>', curtoken) or re.search(r'=', curtoken) or re.search(r'<', curtoken) or re.search(r'\)', curtoken) or re.search(r'\(', curtoken) or re.match(r'[%s][%s]+' % (re.escape(string.punctuation),re.escape(string.punctuation)) , curtoken) or (curtoken == '\"' and (countquote <= 1 or cleantext[0] == '\"')) or (i < len(tokens) - 3 and countquote > 1 and tokens[i+1][0] == '@' and tokens[i+2] == ':'):
		#if curtoken == '!' or curtoken == '?' or curtoken == '.' or curtoken == '--' or curtoken == '<3' or curtoken == ':' or curtoken[0] == ':' or curtoken[0] == ')' or curtoken[0] == '(':
			if len(senttokens) > 1 :
				senttext = ' '.join(senttokens)
				sents.append(senttext)
			senttokens = []
	
	if len(senttokens) > 1:
		senttext = ' '.join(senttokens)
		sents.append(senttext)        
	return sents

# secondary emoticons and punctuation remove, also get rid of very short sentences
def cleanSent(sentence) :
	
	# remove emoticons
	sentence = re.sub(r'[:=]-?[\)\(DPdp]', r'', sentence)
	sentence = re.sub(r'\(-?[:=]', r'', sentence)
	sentence = re.sub(r'<3', r'', sentence)
	tokens = filterTweetText(sentence).strip().split()

	noword = 0
	noword2 = 0
	for i, token in enumerate(tokens) :
		if re.match(r'[a-zA-Z\'][a-zA-Z\']+$', token) :
			noword += 1
		if not re.match(r'[%s]+$' % re.escape(string.punctuation), token) :
			noword2 += 1
	if noword < 2 or noword2 < 3:
		return None
			
	
	#remove punctuations at the end of each sentence
	for i in range(0 , len(tokens)) :
		lasttoken = tokens.pop()
		if lasttoken == '?' or lasttoken == '!' or lasttoken =='.' or (not re.match(r'[%s]+$' % re.escape(string.punctuation), lasttoken)) and (not (re.match(r'#', lasttoken) )):
			tokens.append(lasttoken)
			break
			
	for i in range(0 , len(tokens)) :
		firsttoken = tokens.pop(0)
		secondtoken = tokens[0].lower()
		if not re.match(r'[%s]+$' % re.escape(string.punctuation), firsttoken):
			tokens.insert(0, firsttoken)
			break
	

	sentence = ' '.join(tokens)
	tokens = filterTweetText(sentence).strip().split()
	sentence = ' '.join(tokens)
	
	return sentence  
