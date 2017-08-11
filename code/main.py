#!/usr/bin/python

################################################################################################
# main.py
# Script for collecting paraphrase candidates that share the same URL in Twitter.
#
# Author: Wuwei Lan
#
# @inproceedings{lan2017continuously,
#  title={A Continuously Growing Dataset of Sentential Paraphrases},
#  author={Lan, Wuwei and Qiu, Siyu and He, Hua and Xu, Wei},
#  booktitle = {Proceedings of The 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP)},
#  year={2017}
#}
################################################################################################

import csv
import datetime
import json
import os

import errno
from twitter import *
import time
import sys
from cookielib import CookieJar
import urllib2
import httplib
import twitter_sentence_spliter as spliter

def notOverlap(sent1, sent2):
	txt1=''
	txt2=''
	for ch in sent1:
		if ch.isalnum():
			txt1=txt1+ch.lower()
	for ch in sent2:
		if ch.isalnum():
			txt2=txt2+ch.lower()
	#print txt1
	#print txt2
	if txt1 in txt2 or txt2 in txt1:
		return False
	else:
		return True

config = {}
execfile("config.py", config)
twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
#
news_accounts=['nytimes','CNN','techcrunch','mashable','BreakingNews','cnnbrk','engadget','FoxNews','MakeUseOf','Slate','AlJazeera','AP','BBCBreaking','BBCWorld','BoingBoing','cbsnews','guardiantech','life','nprpolitics','abc','themoment','davos']
yesterday=datetime.datetime.now() - datetime.timedelta(days=1)
#print yesterday.year,yesterday.month,yesterday.day
filename=time.strftime("%Y-%m-%d")+'_en.txt'
extraFilename=time.strftime("%Y-%m-%d")+'_en.json'
htmlfolder=time.strftime("%Y-%m-%d")+'_en/'
#pwd="/Users/lan/Documents/research/PIT/"
pwd='/home/lan/' #your file folder
num = 1
for user in news_accounts:
	#with open(filename, 'a+') as f:
	#	f.write('----------------'+user+'----------------')
	#	f.write('\n')
	results = twitter.statuses.user_timeline(screen_name = user,count=1)
	if len(results)==0:
		continue
	latest_tweet=results[0]
	latest_id=latest_tweet['id_str']
	time_line=latest_tweet['created_at'].split()
	loop_flag=True
	while loop_flag:
		results = twitter.statuses.user_timeline(screen_name=user, max_id=latest_id, count=200)
		for tweet in results:
			latest_id=tweet['id_str']
			time_line = tweet['created_at'].split()
			latest_id=results[-1]['id_str']
			if int(time_line[2]) == yesterday.day:
				loop_flag = False
				break
		latest_id=tweet['id_str']
	latest_id=tweet['id_str']
	#with open(filename, 'a+') as f:
	#	f.write(tweet['created_at'].encode('UTF-8'))
	#	f.write('\n')
	loop_flag=True
	real_urls=[]
	while loop_flag:
		time.sleep(5)
		results=twitter.statuses.user_timeline(screen_name = user,max_id=latest_id,count=200)
		if len(results)>0:
			for tweet in results:
				if len(tweet['entities']['urls']) >= 1:
					url = tweet['entities']['urls'][0]['url']
					txt = spliter.splitCleanTweet2Sents(tweet['text'])
					original_sentence = ''
					for sentence in txt:
						original_sentence = original_sentence + sentence + ' '
					if len(original_sentence.split())<=6:
						continue
					#print tweet['text']
					#print url
					try:
						time.sleep(5)
						cj = CookieJar()
						opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
						result = opener.open(url)
						real_url = result.geturl()
						if real_url.find('.html')!=-1:
							real_url=real_url[:real_url.find('.html') + 5]
						#elif real_url.find('&')!=-1:
						#	real_url=real_url[:real_url.find('&')]
						#elif real_url.find('?')!=-1:
						#	real_url=real_url[:real_url.find('?')]
						#print real_url
						if real_url in real_urls:
							continue
						query=twitter.search.tweets(q =real_url ,lang="en",count="100")
						real_urls.append(real_url)
						if len(query['statuses'])>0:
							paraphrase_candidate=[]
							extraInfo = []
							for query_tweet in query["statuses"]:
								raw_txt=query_tweet['text']
								#print raw_txt
								txt=spliter.splitCleanTweet2Sents(raw_txt)
								#txt=spliter.filterUniqSentSet(txt)
								final_sentence=''
								for sentence in txt:
									final_sentence=final_sentence+sentence+' '
								if len(final_sentence.split())<=6:
									continue
								if notOverlap(final_sentence,original_sentence):
									counter=0
									for element in paraphrase_candidate:
										if notOverlap(element,final_sentence):
											counter+=1
									if counter==len(paraphrase_candidate):
										paraphrase_candidate.append(final_sentence)
										extraInfo.append(json.dumps(query_tweet))
						if len(query['statuses'])==100:
							searchflag=True
							searchlatestid=query['statuses'][-1]['id_str']
							while searchflag:
								time.sleep(5)
								query = twitter.search.tweets(q=real_url, lang="en", count="100", max_id=searchlatestid)
								if len(query['statuses']) > 0:
									for query_tweet in query["statuses"]:
										raw_txt = query_tweet['text']
										txt = spliter.splitCleanTweet2Sents(raw_txt)
										final_sentence=''
										for sentence in txt:
											final_sentence = final_sentence + sentence + ' '
										if len(final_sentence.split()) <= 6:
											continue
										if notOverlap(final_sentence,original_sentence):
											counter = 0
											for element in paraphrase_candidate:
												if notOverlap(element, final_sentence):
													counter += 1
											if counter == len(paraphrase_candidate):
												paraphrase_candidate.append(final_sentence)
												extraInfo.append(json.dumps(query_tweet))
												if len(paraphrase_candidate)>=200:
													searchflag=False
													break
								if len(query['statuses'])==100:
									searchlatestid=query["statuses"][-1]['id_str']
								else:
									searchflag=False
						if len(query['statuses'])>0:
							#paraphrase_candidate=spliter.filterUniqSentSet(paraphrase_candidate)
							#if len(paraphrase_candidate)<=20:
							#	continue
							with open(filename, 'a+') as f:
								temp=tweet['text'].encode('UTF-8')
								temp=temp.replace('\n','')
								temp=temp.replace('\r','')
								f.write('('+'NO.'+str(num)+',Set size:'+str(len(paraphrase_candidate)+1)+','+temp+','+str(real_url)+')')
								f.write('\n')
								f.writelines('%s\n' % original_sentence.encode('UTF-8'))
							with open(extraFilename,'a+') as f:
								temp = tweet['text'].encode('UTF-8')
								temp = temp.replace('\n', '')
								temp = temp.replace('\r', '')
								f.write('(' +user+ ','+'NO.'+str(num)+',Set size:'+str(len(extraInfo)+1) + ',' + temp + ','+str(real_url)+')')
								f.write('\n')
								f.writelines(json.dumps(tweet))
								f.write('\n')
							for item in paraphrase_candidate:
								with open(filename, 'a+') as f:
									f.writelines('%s\n' % item)
								with open(extraFilename,'a+') as f2:
									temp=extraInfo[paraphrase_candidate.index(item)]
									f2.writelines(temp)
									f2.writelines('\n')
							with open(filename,'a+') as f:
								f.write('\n')
							with open(extraFilename,'a+') as f2:
								f2.write('\n')
							page_content=result.read()
							#print page_content
							htmlpath = os.path.join(pwd,htmlfolder)
							if not os.path.exists(os.path.dirname(htmlpath)):
								os.makedirs(os.path.dirname(htmlpath))
							with open(os.path.join(htmlpath,str(num)+'.html'),'w') as f:
								f.write(page_content)
							num += 1
							#sys.exit()
					except urllib2.HTTPError, e:
							print 'HTTPError = ' + str(e.code)
					except urllib2.URLError, e:
							print 'URLError = ' + str(e.reason)
					except httplib.HTTPException, e:
							print  'HTTP Exception.'
					except Exception:
							import traceback
							print 'Generic exception.\n'
							print traceback.format_exc()
					time_line=tweet['created_at'].split()
					if int(time_line[2])!=yesterday.day:
						loop_flag=False
						break
				latest_id = tweet['id_str']
		else:
			print 'No tweets found for this ID: %s'%latest_id
			sys.exit()
	#with open(filename, 'a+') as f:
	#	f.write(tweet['created_at'].encode('UTF-8'))
	#	f.write('\n')