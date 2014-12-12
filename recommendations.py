#!/usr/bin/python

import json
import pprint
import apriori

pp = pprint.PrettyPrinter(indent=4)
users_filename = "./yelp/sm_user.json"
reviews_filename = "./yelp/sm_review.json"

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

    for review in reviews:
        author = review["user_id"]
        business = review["business_id"]
        stars = review["stars"]

        if author in dataset:
            dataset[author]["reviews"].append({"business_id": business, "stars": stars})
        else:
            dataset[author] = {"reviews": []}
            dataset[author]["reviews"].append({"business_id": business, "stars": stars})
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

def find_recs(user):








