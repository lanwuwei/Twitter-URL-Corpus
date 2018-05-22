## News
Currently this repository contains 3-month raw data sample, and our 1-year URL data is available now: 2,869,657 candidate pairs. Please check our [paraphrase website](https://languagenet.github.io/) to download dataset. 

## Paraphrase-dataset
This repository contains code and data used in the following paper, please cite if you use it for your research:

	@inproceedings{lan2017continuously,
	  author     = {Lan, Wuwei and Qiu, Siyu and He, Hua and Xu, Wei},
  	  title      = {A Continuously Growing Dataset of Sentential Paraphrases},
  	  booktitle  = {Proceedings of The 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP)},
  	  year       = {2017},
	  publisher  = {Association for Computational Linguistics},
	  pages      = {1235--1245},
	  location   = {Copenhagen, Denmark}
  	  url        = {http://aclweb.org/anthology/D17-1127}
  	} 

## A few notes
1. Put your own Twitter keys into config.py and modify line 59 in main.py before running the code.
2. Training and testing file is the subset of raw data with human annotation, both files have the same format, each line contains: sentence1 \tab sentence2 \tab (n,6) \tab url
3. For each sentence pair, there are 6 Amazon Mechanical Turk workers annotating it. 1 representa paraphrase and 0 represents non-paraphrase. So totally n out 6 workers think the pair is paraphrase. If n<=2, we treat them as non-paraphrase; if n>=4, we treat them as paraphrase; if n==3, we discard them.
4. After discarding n==3, we can get 42200 for training and 9324 for testing.

## License
It is released for non-commercial use under the CC BY-NC-SA 3.0 license. Use of the data must abide by the Twitter Terms of Service and Developer Policy.
