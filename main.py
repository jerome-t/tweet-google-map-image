#!/usr/bin/env python

import csv
import random
import requests
import json
import shutil
import tweepy
from tweepy import OAuthHandler
import re
from pprint import pprint

#global variables
consumer_key = 'your_key'
consumer_secret = 'your_secret'
access_token = 'your_token'
access_secret = 'your_secret'
google_api_key = "your_key"




# Define the CSV file and size


def commune_random():
    # Choose a random commune from the list
    communes_list = "./20170402_communes-list.csv"
    filesize = 3431
    offset = random.randrange(filesize)
    with open(communes_list) as f:
        f.seek(offset)
        f.readline()
        my_choice = f.readline()
        return(my_choice)

def get_google(my_choice):
    #Get the photoref-ID from Google
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query":my_choice,"key":google_api_key}
    headers = {'Cache-Control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    photoref_answer = json.loads(response.text)
    try:
        if 'You have exceeded your daily request quota for this API' in photoref_answer['error_message']:
            photoremark_name = "API Quota limit exceeded"
            photoremark_url = " - "
            return(photoremark_name, photoremark_url)
    except:
        try:
            photoref = photoref_answer["results"][0]["photos"][0]["photo_reference"]
            photoremark = photoref_answer["results"][0]["photos"][0]["html_attributions"][0]
        except:
            photoremark_name = "No photo"
            photoremark_url = "No remark"
            return(photoremark_name, photoremark_url)

        # Extract name and url from the photoremark:
        photoremark_url = photoremark.split(">")[0]
        photoremark_url = photoremark_url[9:-1]
        photoremark_name = photoremark.split(">")[1]
        photoremark_name = photoremark_name[:-3]

        #Get the photo itself from Google and copy it locally:
        photo_url = "https://maps.googleapis.com/maps/api/place/photo"
        photo_querystring = {"maxwidth":"1600","photoreference":photoref,"key":google_api_key}
        headers = {'Cache-Control': "no-cache"}
        photo_response = requests.request("GET", photo_url, headers=headers, params=photo_querystring, stream=True)

        if photo_response.status_code == 200:
            with open("./switzerland_pix_of_the_day.jpg", 'wb') as f:
                shutil.copyfileobj(photo_response.raw, f)
                print("--- OK, we have a picture ---")
                return(photoremark_name, photoremark_url)
        else:
            print("--- Unable to download image ---")
            photoremark_name = "No photo"
            return


#Post the commune name, photo and credits on Twitter:
def post_tw(my_choice, photoremark_name, photoremark_url, my_commune, my_canton):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    tw_message = """The #Switzerland Picture of the day is from: {0}\r
Credits: {1} - {2}\r
Images may be subject to copyright\n
#Switzerland_pix #{3} #{4}""".format(my_choice, photoremark_name, photoremark_url, my_commune, my_canton)
    print(tw_message)
    # --- Here we post the Tweet - Comment if needed ---
    api.update_with_media("./switzerland_pix_of_the_day.jpg", status=tw_message)
    # --- end Tweet post ---




if __name__ == "__main__":
    my_choice = commune_random()
    my_commune, my_canton = my_choice.split(",")
    print("La commune du jour est: {0}, dans le canton de {1}".format(my_commune, my_canton))
    print("=" * 60)
    photoremark_name, photoremark_url = get_google(my_choice)
    print("Credit name:", photoremark_name)
    print("Credit URL:", photoremark_url)
    print("=" * 60)
    while photoremark_name == "No photo":
        print("*" * 60)
        print("Start again...")
        photoremark_name = ""
        my_choice = ""
        my_choice = commune_random()
        my_commune, my_canton = my_choice.split(",")
        photoremark_name, photoremark_url = get_google(my_choice)
        print(photoremark_name)
    post_tw(my_choice, photoremark_name, photoremark_url, my_commune, my_canton)
    print("Tweet posted!")
    print("=" * 60)
    
    
