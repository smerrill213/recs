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
nmtrx = ''
the_matrix = ''
dataset = ''
bus_ids = {} # integer to id
bus_ints = {} # id to integer
bus_names = {} # from weird id string to business name
user_ids = {}
user_ints = {}
threshold = .3

# First make dataset by making lists for each user of places they visited and rated highly and maybe even lowly
# So maybe have each place plus its rating by that user

# Function: make dataset
def make_dataset(users_filename, reviews_filename):

#    with open(users_filename, 'rb') as users_file:
#        user_data = users_file.read()
#
#    users = json.loads(user_data)

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
            if business not in bus_ints:
                bus_ids[j] = business
                bus_ints[business] = j
                j += 1
        else:
            dataset[author] = {"reviews": []}
            user_ids[i] = author
            user_ints[author] = i
            i += 1
            dataset[author]["reviews"].append({"business_id": business, "stars": stars})
            if business not in bus_ints:
                bus_ids[j] = business
                bus_ints[business] = j
                j += 1
    return dataset
#    pp.pprint(dataset)
#    print json.dumps(dataset, indent = 4)

dataset = make_dataset(users_filename, reviews_filename)

def make_utility_mtrx():
    num_users = len(user_ids)
    num_bus = len(bus_ids)
    mtrx = [[0 for j in range(num_bus)] for i in range(num_users)]
    for user in dataset:
        if user in user_ints:
            userint = user_ints[user]
            for review in dataset[user]["reviews"]:
                busint = bus_ints[review["business_id"]]
                stars = review["stars"]
                mtrx[userint][busint] = stars
        else:
            print "User {} not in user_ids".format(user)
    return mtrx

umtrx = make_utility_mtrx()
the_matrix = umtrx

def normalize_mtrx(mtrx):
    nmtrx = [[0 for j in range(len(mtrx[0]))] for i in range(len(mtrx))]
    for i in range(len(mtrx)):
        sum = 0
        ct = 0
        for j in range(len(mtrx[0])):
            if mtrx[i][j] != 0:
                sum += mtrx[i][j]
                ct += 1
        avg = sum / ct
        for j in range(len(mtrx[0])):
            if mtrx[i][j] != 0:
                nmtrx[i][j] = mtrx[i][j] - avg
    return nmtrx 

nmtrx = normalize_mtrx(umtrx)
the_matrix = nmtrx

#i = 0
#for u in umtrx:
#    if i > 20:
#        break
#    print u
#    print "\n"

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

#umtrx = make_util_mtrx()
#for user in umtrx:
#    print "{}\n".format(user)

def cos_sim(user1, user2): # user1 and user2 are id numbers (integers)
    numerator = 0
    for i in range(len(the_matrix[0])):
        if the_matrix[user1][i] != 0 and the_matrix[user2][i] != 0:
            numerator += the_matrix[user1][i] * the_matrix[user2][i]
    denom = 0
    user1sumsq = 0
    user2sumsq = 0
    for i in range(len(the_matrix[0])):
        user1sumsq += the_matrix[user1][i] * the_matrix[user1][i]
        user2sumsq += the_matrix[user2][i] * the_matrix[user2][i]
        i += 1
    denom += sqrt(user1sumsq) * sqrt(user2sumsq)
    if denom == 0:
        return 0.0
    else:
        return numerator / denom

#for i in range(100):
#    for j in range(300, 200, -1):
#        sim = cos_sim(i, j)
#        if abs(sim) >= 0.001 and abs(sim - 1.0) >= 0.001:
#            print "cos_sim for users {} and {}: {}".format(i, j, sim)

def find_similar_users(user): # user is the integer id
    sim_users = []
    for user2 in dataset:
        cossim = cos_sim(user, user_ints[user2])
        if user != user2 and cossim >= threshold: #and abs(cossim - 1.0) >= 0.001:
            sim_users.append((user_ints[user2], cossim))
    return sim_users #this is a list of tuples of (user integer, similarity) 

#for i in range(10):
#    simusers = find_similar_users(i)
#    if len(simusers) != 0:
#        print "Similar users to {}:\n".format(i)
#        for user in simusers:
#            print "User: {}, similarity: {}".format(user[0], user[1])
#        print "\n"

def favs(user): # user is the integer id
    favs = [] 
    for bus in dataset[user_ids[user]]["reviews"]:
        if bus["stars"] >= 0: # if they rated it above their average
            favs.append(bus["business_id"]) 
    return favs

def find_recommendations(user):
    recs = []
    sim_users = find_similar_users(user)
    userfavs = favs(user)
    for user in sim_users:
        favslist = favs(user[0])
        for f in favslist:
            if f not in recs and f not in userfavs:
                recs.append(f)
    return recs

#for i in range(50):
#    print "Similar users to user {}: {}".format(i, find_similar_users(i))

def make_bus_dict():
    
    with open(bus_filename, 'rb') as bus_file:
        bus_data = bus_file.read()

    businesses = json.loads(bus_data)

    for b in businesses:
        id = b["business_id"]
        name = b["name"]
        bus_names[id] = name

make_bus_dict()

def bus_name(busid):
    if busid in bus_names:
        return bus_names[busid]    
    else:
        return busid

for i in range(500, 100, -5):
    favslist = favs(i)
    favs_string = ''
    for f in favslist:
        bname = bus_name(f)
        favs_string += bname + ", "
    recs = find_recommendations(i)
    recs_string = ''
    for r in recs:
        bname = bus_name(r)
        recs_string += bname + "\n"
    if len(recs) != 0:
        print "Because user {} liked {}, we recommend the following businesses: \n{}\n".format(i, favs_string, recs_string)

