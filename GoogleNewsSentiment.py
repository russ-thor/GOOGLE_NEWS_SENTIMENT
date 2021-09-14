#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Russ T
# Created: September 2021
# See READ_ME.doc in repository
# Google search tips: https://stenevang.wordpress.com/2013/02/22/google-advanced-power-search-url-request-parameters/

# Imports
import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# variables

# SET SEARCH TOPIC(S), HISTORICAL RANGE TO ANALYZE, TITLE
# *****************************************************************

search_topic_list = ['Canada Conservatives']
historical_time_range = '&tbs=cdr:1,cd_min:9/13/2020,cd_max:9/13/2021'  # update dates only
historical_time_range_title = 'Sentiment (Last Year)'

# *****************************************************************

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/70.0.3538.77 Safari/537.36'
}
analyzer = SentimentIntensityAnalyzer()  # VADER sentiment class
today = datetime.date.today()
last_week = '&tbs=qdr:w'  # Google Search: results from last week


# analyze sentiment of 100 Google News results - inputs are search term and time frame (1 week + 1 year are defaults)


def date_string_type_to_time_type(date_string):
    """This f(x) will convert a string date into a date object which is needed as the data information in Google News
    is in an inconsistent format. Standard date-time format is needed to effectively plot a time series bar chart"""

    if date_string.find("min") != -1:
        return today

    if date_string.find("hour") != -1:
        return today

    elif date_string.find("1 day ago") != -1:
        return today - datetime.timedelta(days=1)
    elif date_string.find("days ago") != -1:
        return today - datetime.timedelta(days=(int(date_string[0])))

    elif date_string.find("1 week ago") != -1:
        return today - datetime.timedelta(weeks=1)
    elif date_string.find("weeks ago") != -1:
        return today - datetime.timedelta(weeks=(int(date_string[0])))

    elif date_string.find("1 month ago") != -1:
        return today - datetime.timedelta(weeks=4)
    elif date_string.find("12 months ago") != -1:
        return today - datetime.timedelta(days=(int(date_string[0:2]) * 30))
    elif date_string.find("11 months ago") != -1:
        return today - datetime.timedelta(days=(int(date_string[0:2]) * 30))
    elif date_string.find("10 months ago") != -1:
        return today - datetime.timedelta(days=(int(date_string[0:2]) * 30))
    elif date_string.find("months ago") != -1:
        return today - datetime.timedelta(days=(int(date_string[0:1]) * 30))

    else:
        date_string = date_string.replace('.', '')
        return datetime.datetime.strptime(date_string, '%b %d %Y').date()


def plot_sentiment_analysis(csv_list, search_topic):
    """This f(x) will take a list of two csv's that get created in the 'google_search_sentiment_analysis' f(x) below
    and plot a comparison of current and historical sentiment, as well as a compound sentiment score time series"""

    # Plot sentiment comparison between timeframes
    print(csv_list)

    # Make plotly subplot figure
    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}], [{'colspan': 2}, None]],
    )

    for i, csv in enumerate(csv_list):
        df = pd.read_csv(csv, encoding='unicode_escape', index_col=False)

        if i == 0:
            fig.add_trace(go.Pie(labels=df['Sentiment'], title=historical_time_range_title), row=1, col=1)

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Sentiment_Compound'],
                    name='COMPOUND SENTIMENT SCORE',
                    mode='markers',
                    marker_color='grey',
                ),
                row=2,
                col=1,
            )

            fig.update_layout(
                title=f"Google News Headline Sentiment - Historical vs Last Week: {search_topic}",
                xaxis_title="Compound Sentiment Timeline",
                yaxis_title="Compound Score",
                height=600,
                width=1200,
                font=dict(family="Courier New, monospace", size=15, color="Black"),
            )

        if i == 1:

            fig.add_trace(go.Pie(labels=df['Sentiment'], title='Sentiment (1 Week)'), row=1, col=2)

    # Save figures
    static_graph = f'{search_topic}_{str(today)}.png'
    dynamic_graph = f'{search_topic}_{str(today)}.html'
    fig.write_html(dynamic_graph)
    fig.write_image(static_graph)

    # Show Plotly graph in browser
    fig.show()


def google_search_sentiment_analysis(search_topic):
    """This f(x) will analyze the sentiment of the historical (user defined range) and last weeks Google News articles.
    The articles will be webscraped from Google and the information and sentiment of each article will be saved in a
    csv"""

    csv_list = []  # To be used for plotting, will include the 1 week and 1 year csv after function completes

    for scenario in [historical_time_range, last_week]:
        time.sleep(5)  # don't want 429 errors while webscraping

        # request data, format html using bs4,
        link = f'https://www.google.com/search?q={search_topic}&tbm=nws&num=100{scenario}'
        req = requests.get(link, headers=headers)
        print('Authentication:', req.status_code)  # 200 means successful
        page_soup = soup(req.text, 'html.parser')

        # iterate through results of Google search and collect individual article data
        for i, article in enumerate(page_soup.find_all('g-card', {'class': "nChh6e DyOREb"})):

            # text needed for writing excel file names
            if scenario == last_week:
                csv_tag = 'last7Days'
            elif scenario == historical_time_range:
                csv_tag = 'historical'

            # Extract article title, publisher, timestamp, http link
            publisher = article.find('div', {'class': "XTjFC WF4CUc"}).text
            title = article.find('div', {'role': "heading"}).text.replace('\n', '')  # replace html <br>'s
            source = article.find('a')['href']
            date_str = article.find('span', {'class': "WG9SHc"}).text.replace(',', '')  # commas cause issues with csv
            date = date_string_type_to_time_type(date_str)

            # Run VADER sentiment scoring of the article title (using polarity_score method)
            sentiment = analyzer.polarity_scores(title)
            sentiment_negative = sentiment['neg']
            sentiment_neutral = sentiment['neu']
            sentiment_positive = sentiment['pos']
            sentiment_compound = sentiment['compound']
            if -0.05 < sentiment_compound < 0.05:
                sentiment_text_score = 'NEUTRAL'
            elif sentiment_compound <= -0.05:
                sentiment_text_score = 'NEGATIVE'
            else:
                sentiment_text_score = 'POSITIVE'

            # print data to terminal for QC
            print(title + '\n' + str(sentiment) + '\n' + source + '\n' + str(date), publisher, '\n')

            # Write article data and sentiment information to csv
            with open(f'{search_topic}_{csv_tag}.csv', 'a') as fileObj:

                # commas in titles interfere with csv export (not replaced above as sentiment analysis considers them)
                title = title.replace(',', '')

                # write headers on first iteration only
                if i == 0:
                    fileObj.write(
                        "Date,Publisher,Title,Sentiment,Sentiment_Compound,Sentiment_Negative,"
                        "Sentiment_Neutral,Sentiment_Positive,Source\n"
                    )

                # write data to row on every iteration
                try:
                    fileObj.write(
                        f'{str(date)},{publisher},{title},{sentiment_text_score},{sentiment_compound},'
                        f'{sentiment_negative},{sentiment_neutral},{sentiment_positive},{source},\n'
                    )
                except:
                    print(f'!!!! article: {i}, {title} not written to csv !!!!')

        csv_list.append(f'{search_topic}_{csv_tag}.csv')

    # call the plot sentiment analysis function to create sentiment graphs/ report out the findings
    plot_sentiment_analysis(csv_list, search_topic)


for search in search_topic_list:
    google_search_sentiment_analysis(search)
