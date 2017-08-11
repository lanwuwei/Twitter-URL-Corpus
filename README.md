# paraphrase-dataset
This repository contains code and data sample used in the following paper:

	@inproceedings{lan2017continuously,
  	  title      = {A Continuously Growing Dataset of Sentential Paraphrases},
  	  author     = {Lan, Wuwei and Qiu, Siyu and He, Hua and Xu, Wei},
  	  booktitle  = {Proceedings of The 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP)},
  	  year       = {2017},
  	  url        = {https://arxiv.org/abs/1708.00391}
  	} 

Please email lan.105@osu.edu for the full dataset. Only sample data is included in this Github repository.

## A few notes
1. Put your own Twitter keys into config.py and modify line 59 in main.py before running the code.
2. Training and testing file is the subset of raw data with human annotation, both files have the same format, each line contains: sentence1 \tab sentence2 \tab (n,6) \tab url
3. For each sentence pair, there are 6 Amazon Mechanical Turk workers annotating it. 1 representa paraphrase and 0 represents non-paraphrase. So totally n out 6 workers think the pair is paraphrase. If n<=2, we treat them as non-paraphrase; if n>=4, we treat them as paraphrase; if n==3, we discard them.
4. After discarding n==3, we can get 42200 for training and 9324 for testing.
