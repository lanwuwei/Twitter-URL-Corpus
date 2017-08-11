# paraphrase-dataset
This repository contains code and data sample used in the following paper:

@inproceedings{xu2013gathering,
  title      = {Gathering and generating paraphrases from {Twitter} with application to normalization},
  author     = {Xu, Wei and Ritter, Alan and Grishman, Ralph},
  booktitle  = {Proceedings of the Sixth Workshop on Building and Using Comparable Corpora (BUCC)},
  year       = {2013},
  url        = {http://aclweb.org/anthology/W/W13/W13-2515.pdf}
}   

Please email lan.105@osu.edu for the full dataset. Only sample data is included in this Github repository.

## A few notes
1. Put your own Twitter keys into config.py and modify line 59 in main.py before running the code.
2. Training and testing file is the subset of raw data with human annotation, both files have the same format, each line contains: sentence1 \tab sentence2 \tab (n,6) \tab url
3. For each sentence pair, there are 6 Amazon Mechanical Turk workers annotating it. 1 representa paraphrase and 0 represents non-paraphrase. So totally n out 6 workers think the pair is paraphrase. If n<=2, we treat them as non-paraphrase; if n>=4, we treat them as paraphrase; if n==3, we discard them.
4. After discarding n==3, we can get 42200 for training and 9324 for testing.
