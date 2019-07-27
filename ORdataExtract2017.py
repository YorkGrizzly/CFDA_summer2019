'This file executes data extraction for the submissions and decisions of ICLR 2017 on Open Review'

import openreview
import pandas as pd
import numpy as np

import re
import urllib.request

client = openreview.Client(baseurl = 'https://openreview.net', username = 'dylanjootw@gmail.com', password = "cfdacfda")


decision2017 = 'ICLR.cc/2017/conference/-/paper.*/acceptance'
# paper type, acceptance, comments of each paper
submission2017 = 'ICLR.cc/2017/conference/-/submission'
# submissions of all papers: abstracts, titles, authors...
#the papers listed in both invitations are identical (all match)

allreview2017 = 'ICLR.cc/2017/conference/-/paper.*/review'
#some papers are not in 'submissions'
officialreview2017 = 'ICLR.cc/2017/conference/-/paper.*/official/review'


#extract data from all decisions
Decision_paperID = []
Decision_decision = []
Decision_comment = []

for note in openreview.tools.iterget_notes(client, invitation = decision2017, details = 'original'):
    Decision_paperID.append(note.forum)
    Decision_decision.append(note.content['decision'])
    Decision_comment.append(note.content['comment'])

#extract data from all submissions and match their decisions
paperID = []
title = []
abstract = []
keyWrd = []
decision = []
comment = []

for note in openreview.tools.iterget_notes(client, invitation = submission2017, details = 'original'):
    paperID.append(note.id)
    title.append(note.content['title'])
    abstract.append(note.content['abstract'])
    keyWrd.append(note.content['keywords'])
    if note.id in Decision_paperID:
        index = Decision_paperID.index(note.id)
        decision.append(Decision_decision[index]) #accept/reject/invite to workshop
        comment.append(Decision_comment[index])

allPapers = pd.DataFrame(data = {'PaperID': paperID, 'Decision': decision, 'Title': title, 'Abstract': abstract, 'Keyword': keyWrd, 'Comment': comment})

allPapers.to_csv('ICLR17_submissions.csv')

#get reviews for papers in submission from official reviews
OReview_paperID = []
OReview_confi = []  #confidence (there are 13 cases with no such entry)
OReview_rating = []
OReview_review = []

for note in openreview.tools.iterget_notes(client, invitation = officialreview2017, details= 'original'):
    if note.forum in paperID:    
        OReview_paperID.append(note.forum)
        try:
            OReview_confi.append(note.content['confidence'][0])
        except:
            OReview_confi.append('')
        OReview_rating.append(note.content['rating'][0])
        OReview_review.append(note.content['review'])

OReviews = pd.DataFrame(data = {'PaperID': OReview_paperID, 'Confidence': OReview_confi, 'Rating': OReview_rating, 'Review': OReview_review})

OReviews.to_csv('ICLR17_Official_Reviews.csv')

#get reviews for papers in submission from all reviews
AReview_paperID = []
AReview_confi = []  #(there are 13 cases with no such entry)
AReview_rating = []        
AReview_review = []

for note in openreview.tools.iterget_notes(client, invitation = allreview2017, details = 'original'):
    if note.forum in paperID:
        AReview_paperID.append(note.forum)
        try:
            AReview_confi.append(note.content['confidence'][0])
        except:
            AReview_confi.append('')
        AReview_rating.append(note.content['rating'][0])
        AReview_review.append(note.content['review'])

AReviews = pd.DataFrame(data = {'PaperID': AReview_paperID, 'Confidence': AReview_confi, 'Rating': AReview_rating, 'Review': AReview_review})

AReviews.to_csv('ICLR17_All_Reviews.csv')


