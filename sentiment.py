from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
sia= SentimentIntensityAnalyzer()
stop_words= set(stopwords.words('english'))
def calculate_sentiment(comment):
    word_tokens= word_tokenize(comment)
    filtered_sentence= [words for words in word_tokens if not words in stop_words]
    filtered_sentence= ' '.join(filtered_sentence)
    score= sia.polarity_scores(filtered_sentence)
    return score
    
calculate_sentiment("Sandra Bullock is a breathtaking actress.")