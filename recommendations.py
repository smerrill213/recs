#!/usr/bin/python

from __future__ import division
import json
import pprint
import apriori
from math import sqrt

pp = pprint.PrettyPrinter(indent=4)
users_filename = "./yelp/sm_user.json"
reviews_filename = "./yelp/sm_review.json"
bus_filename = "./yelp/sm_business.json"

umtrx = ''
dataset = ''
bus_ids = {} # integer to id
bus_ints = {} # id to integer
user_ids = {}
user_ints = {}
threshold = .3

# First make dataset by making lists for each user of places they visited and rated highly and maybe even lowly
# So maybe have each place plus its rating by that user

# Function: make dataset
def make_dataset(users_filename, reviews_filename):

    with open(users_filename, 'rb') as users_file:
        user_data = users_file.read()

    users = json.loads(user_data)

    with open(reviews_filename, 'rb') as reviews_file:
        review_data = reviews_file.read()

    reviews = json.loads(review_data)

    # If user not in dictionary, add user and a corresponding 
    # list of tuples of establishment, review
    # dataset[user] = {profile: {any user info}, reviews: [{business_id:____, stars: _____}]}

    dataset = {}
    assert type(dataset) is dict

#    for user in users:
#        id = user["user_id"]
#        dataset[id] = {"reviews": []} 

    i = 0
    j = 0
    
    for review in reviews:
        author = review["user_id"]
        business = review["business_id"]
        stars = review["stars"]
        
        if author in dataset:
            dataset[author]["reviews"].append({"business_id": business, "stars": stars})
            if business not in bus_ids.values():
                bus_ids[j] = business
                bus_ints[business] = j
                j += 1
        else:
            dataset[author] = {"reviews": []}
            user_ids[i] = author
            user_ints[author] = i
            i += 1
            dataset[author]["reviews"].append({"business_id": business, "stars": stars})
            if business not in bus_ids.values():
                bus_ids[j] = business
                bus_ints[business] = j
                j += 1
    return dataset
#    pp.pprint(dataset)
#    print json.dumps(dataset, indent = 4)

dataset = make_dataset(users_filename, reviews_filename)

def make_apriori_dataset(data):
    dataset = []
    assert type(data) is dict
    for user, info in data.iteritems():
        row = []
        for review in info["reviews"]:
            row.append(review["business_id"])
        dataset.append(row)
    return dataset

#dataset = make_apriori_dataset(dataset)

#L, support_data = apriori.apriori(dataset, minsupport = 0.0015)

#for entry in L[0]:
#    print entry

def make_util_mtrx():
    mtrx = [[0 for bus in range(len(bus_ids))] for user in range(len(user_ids))]
    assert len(mtrx) == len(user_ids)
    assert len(mtrx[0]) == len(bus_ids)
    for user in dataset:
        for review in dataset[user]["reviews"]:
            usernum = user_ints[user]
            busnum = bus_ints[review["business_id"]]
            mtrx[usernum][busnum] = review["stars"]
    return mtrx 

make_util_mtrx()

def cos_sim(user1, user2): # user1 and user2 are id numbers (integers)
    numerator = 0
    for i in range(len(umtrx[0]):
        if umtrx[user1][i] != 0 and umtrx[user2][i] != 0:
            numerator += umtrx[user1][i] * umtrx[user2][i]
    denom = 0
    user1sumsq = 0
    user2sumsq = 0
    for i in range(len(umtrx[0])):
        user1sumsq += umtrx[user1][i] * umtrx[user1][i]
        user2sumsq += umtrx[user2][i] * umtrx[user2][i]
        i += 1
    denom += sqrt(user1sumsq) * sqrt(user2sumsq)
    if denom == 0:
        return 0
    else return numerator / denom

#def find_recommendations(user):
#
#def favs(user):
#
#def find_similar_users(user):
#

#def normalize_mtrx(mtrx) 

 

