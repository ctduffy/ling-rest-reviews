###################
# Linguistic analysis of Restaurant reviews
# Author: Clara Duffy
# Circa: 2019
###################
import numpy
import nltk
import json
import string

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

def add_tokens(st):
  st = st.lower()
  exclude = set(string.punctuation)
  st = ''.join(ch for ch in st if ch not in exclude)
  temp = nltk.word_tokenize(st)
  for each in temp:
    if each in toks:
      toks[each] = toks[each] + 1
    else:
      toks[each] = 1

for rest in parsed_json["restaurants"]: #gets all the info I want.
  # print rest["name"]
  # print rest["rating"] #goes from 1.0-5.0 (theoretically, but actually starts at 2.5)
  # print rest["price"] #goes from 1-4
  # rest_tokens[rest["name"]] = {}
  # rest_tokens[rest["name"]] = {'rating': rest["rating"], 'price': rest["price"], 'reviews': [] }
  for revs in rest["reviews"]:
    #adds each review string to a dict of all words
    add_tokens(revs["review_text"])
    # tokens(revs["review_text"])


freq = nltk.FreqDist(toks)


print freq.most_common(40)

#print rest_tokens


# print type(parsed_json["restaurants"][0]["reviews"][0]["review_text"])

# for each in parsed_json["restaurants"][0]["reviews"][0]:
#   print each

# print parsed_json["restaurants"][0]["reviews"][0]["review_text"].split()


