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

# example output

# References

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

