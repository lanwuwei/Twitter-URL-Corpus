1, This is the sample of raw data for EMNLP 2017 “A Continuously Growing Dataset of Sentential Paraphrases”, email lan.105@osu.edu for the whole data.

2, For each day, there is a *.txt file, *.tar.gz file and a corresponding file folder. The detail for each file is as the following:
*.txt: it contains multiple sets, each set has a bunch of tweets sharing the same URL. The first line of each set is (NO.#, Set size:#, original tweet, URL), the following lines are tweets that share the same URL as the original tweet.
*.tar.gz: it contains a json file, which has whole information for each tweet in *.txt file.
file folder: it contains original website for each URL.