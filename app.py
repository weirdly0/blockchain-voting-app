from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import time
from markupsafe import Markup
import tweepy
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'reds209ndsldssdsljdsldsdsljdsldksdksdsdfsfsfsfis'
#session.init_app(app)

positive = 0
negative = 0
neutral = 0

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHI1xAEAAAAAsBXuf%2BRl%2Fe0QHS7DW4QyP%2FQmkw8%3DMOUIM11VeXtuF04uesl6IqUxG40a0ShxWVcasoQF3e9KFLp9z0'  # Add your bearer token here

@app.route('/')
def home():
    if not session.get('searched'):
        return render_template('search.html')
    else:
        labels = ["Positive", "Negative", "Neutral"]
        global positive
        global negative
        global neutral
        values = [positive, negative, neutral]
        colors = ["#8bc34a", "#ff5252", "#9e9e9e"]
        session['searched'] = False
        return render_template('chart.html', set=zip(values, labels, colors))


@app.route('/search', methods=['POST'])


def do_search():
    if request.form['search_query'] == '':
        flash('Search Query cannot be empty!')
        session['searched'] = False
    elif request.form['max_tweets'] == '':
        flash('Max Tweets cannot be empty!')
        session['searched'] = False
    elif not request.form['max_tweets'].isdigit():
        flash('Max Tweets should be a number!')
        session['searched'] = False
    else:
        hash_tag = request.form['search_query']
        number = int(request.form['max_tweets'])
        max_results = min(number, 100)

        try:
            from tweepy import Client
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            from collections import Counter
            import nltk

            # Twitter API v2 Client
            client = Client(bearer_token=bearer_token)

            # Include language filter in the query
            query = f"{hash_tag} lang:en"

            dataset = []
            total_fetched = 0
            next_token = None

            # Loop to handle pagination and respect rate limits
            while total_fetched < number:
                try:
                    tweets = client.search_recent_tweets(
                        query=query,
                        max_results=max_results,
                        tweet_fields=['text', 'created_at'],
                        next_token=next_token
                    )

                    if tweets.data:
                        dataset.extend([tweet.text for tweet in tweets.data])
                        total_fetched += len(tweets.data)
                        next_token = tweets.meta.get('next_token')
                    else:
                        break  # Exit loop if no more tweets are found

                    print(f"Fetched {total_fetched}/{number} tweets")

                except tweepy.TooManyRequests:
                    print("Rate limit reached. Sleeping for 1 minutes...")
                    time.sleep(60)  # Sleep for 1minute
                except Exception as e:
                    print(f"Error fetching tweets: {e}")
                    break

            # Sentiment Analysis
            nltk.download('vader_lexicon')
            sid = SentimentIntensityAnalyzer()
            counter = Counter()

            for data in dataset:
                ss = sid.polarity_scores(data)
                if ss['compound'] >= 0.05:
                    counter['positive'] += 1
                elif ss['compound'] <= -0.05:
                    counter['negative'] += 1
                else:
                    counter['neutral'] += 1

            global positive, negative, neutral
            positive = counter['positive']
            negative = counter['negative']
            neutral = counter['neutral']

            session['searched'] = True

        except Exception as e:
            flash(f"Error fetching tweets: {e}")
            print(f"Error: {str(e)}")
            session['searched'] = False

    return home()



app.secret_key = 'abcdefghijk'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
