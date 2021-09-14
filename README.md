#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Russ T
# Created: September 2021
# See READ_ME.doc in repository
# Google search tips: https://stenevang.wordpress.com/2013/02/22/google-advanced-power-search-url-request-parameters/

# description 
This project employs Beautiful Soup to webscrape user defined Google News articles (n=100, largest amount able to be displayed on one Google page), analyze the sentiment of the headline using the Valence Aware Dictionary and sEntiment Reasoner program (VADER - https://github.com/cjhutto/vaderSentiment), and plot the results using Plotly. An excel spreadsheet of the articles title, link, date, setiment rank (positive, nuetral, negative), and sentiment compound score (1- to +1) is also exported which allows the user to assess how well VADER is doing at classifying the sentiment for the chosesn subject.

# installation 
- pip install pandas 
- pip install bs4
- pip install plotly==5.2.1
- pip install vaderSentiment

# function descriptions

- date_string_type_to_time_type
The date_string_type_to_time_type function (called from the main google_search_sentiment_analysis function) takes the news articles string date and converts it into a date object. The string input from the articles can come in many forms (1 day ago, 2 weeks ago, 2 months ago, 1 hour ago, etc.) The output of this function is always in the YYYY/MM/DD format necessary for plotting the sentiment in a time series plot.

- plot_sentiment_analysis 
The plot_sentiment_analysis function (called from the main google_search_sentiment_analysis function) takes two csv inputs: 1 week & the user defined historical range. It plots two pie charts on the top half of the graph which show the negative, nuetral, and positive sentiment for each timeframe and one time series chart on the bottom half which shows the compound sentiment score of each article over the historical time frame. Titles and labels are dynamically updated and a static image and dynamic html link of the graph is saved into the projects working directory.

- google_search_sentiment_analysis 
The google_search_sentiment_analysis is the primary project function which uses Requests and Beautiful Soup to webscrape 100 news article results from Google. It then pulls out the title, publisher, link, and date before running a sentiment analysis on the title using VADER. All of this info is then written to a csv for each timeframe scenario.

# example output

# References

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

