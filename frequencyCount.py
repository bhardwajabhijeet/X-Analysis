from pyspark import SparkContext

sc.stop()
sc = SparkContext("local", "Frequency Count of given words using Map Reduce")

word_list = ["education", "canada", "university", "dalhousie", "expensive", "good school", "faculty", "computer", "science", "good schools", "bad school","bad schools", "poor school", "poor schools", "graduate"]

#performs word frequency count on tweets data
tweet_words = sc.textFile("clean_tweets_data.txt").flatMap(lambda line: line.split(" "))
tweet_words_count = tweet_words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
sorted_tweet_words = tweet_words_count.sortBy(lambda x: x[1], False)
with open("tweet_wordcount_results.txt", 'a') as file:
    for word, count in sorted_tweet_words.toLocalIterator():
        if word in word_list:
            file.write(word + ":" + str(count) + ",\n")
            print(word + ":" + str(count))
