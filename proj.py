###################
# Linguistic analysis of Restaurant reviews
# Author: Clara Duffy
# Circa: 2019
###################
import numpy
import nltk
import json
import string
import math
import matplotlib.pyplot as plt
import pandas
import csv


tripreviews = open('tripreviews.json').read()

#comment: this will print word strings with "u" below them to denote unicode.


parsed_json = json.loads(tripreviews)
# contains:
  # total_review_count -> 14700 (100 for each restaurant)
  # restaurant_count -> 147
  # restaurants -> list of restaurants
    # restaurant -> dict with: rating, parking_garage, tel, meal_lunch, options_organic, parking, parking_free, cuisine, meal_dinner, locality, parking_valet, meal_cater, latitude, email, website, fax, options_healthy, parking_validated, meal_takeout, meal_breakfast, price, hours, address, smoking, parking_lot, parking_street, trip_advisor_url, options_lowfat, name, country, region, wifi, accessible_wheelchair, longitude, reviews, meal_deliver, options_vegan, options_glutenfree, options_vegetarian
      # reviews: list containing reviews
        #review: dict with review_website, review_text, review_rating, review_title, review_date, review_url
toks = {}


def add_tokens(st, d_o_f):
  st = st.lower()
  exclude = set(string.punctuation)
  st = ''.join(ch for ch in st if ch not in exclude)
  temp = nltk.word_tokenize(st)
  # if not ("count" in d_o_f):
    # d_o_f["count"] = 0
  for each in temp:
    if each in d_o_f:
      d_o_f[each] = d_o_f[each] + 1
      # d_o_f["count"] = d_o_f["count"] + 1
    else:
      # d_o_f["count"] = d_o_f["count"] + 1
      d_o_f[each] = 1
  return d_o_f


categories_dict = {}

# 1. create dictionary with section for each rating(rounded up) and price (already round). This will be sorted by price, and each price will have 3 inner categories.

i = 0

freq = {}

for rest in parsed_json["restaurants"]:
  pr = rest["price"] #should go from 1-4
  rat = rest["rating"] #should now go from 3-5
  if not (pr, rat) in categories_dict:
    categories_dict[pr, rat] = {}
  for revs in rest["reviews"]:
    categories_dict[pr, rat].update(add_tokens(revs["review_text"], categories_dict[pr, rat]))
    # categories_dict[pr, rat].append(add_tokens(revs["review_text"]))
    # freq = nltk.FreqDist(categories_dict[pr, rat])

    # for each in freq.most_common(50):
    #   print each

count = 0

common_freqs = []
#can change to below to get only integers, also must change corresponding above line to: (or something similar to get rating rounded to ints # rat = int(math.ceiling(rest["rating"])) #should now go from 3-5
#with open('trip_file.csv', mode='w') as tfile:
with open('trip_file_floats.csv', mode='w') as tfile:
  twriter = csv.writer(tfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  twriter.writerow(['dollars', 'stars', 'first', 'second', 'third', 'fourth', 'num_words', 'diff_words'])

  for d in categories_dict:
    print "//////////", count, "//////////", d
    freq[d] = nltk.FreqDist(categories_dict[d])
    temp = freq[d].most_common(10)
    twriter.writerow([d[0], d[1], temp[0], temp[1], temp[2], temp[3], freq[d].N(), freq[d].B()])
    count += 1
