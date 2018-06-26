# tweet-google-map-image
This is a very basic Tweeterbot to publish an image from Google map.
I made this to train myself to the basics of Python scripting and API calls. Please be indulgent on the syntax.

The script take a random Swiss commune name from a CVS file, I build it from the official Switzerland administration list here:
https://www.bfs.admin.ch/bfs/fr/home/statistiques/catalogues-banques-donnees/publications.assetdetail.2245010.html

The script search the commune into Google map and extract the picture reference of this place and the author name of the picture.
API example: https://maps.googleapis.com/maps/api/place/textsearch/json?query=123+main+street&key=YOUR_API_KEY

Then it download the photo locally with another API call.

Finally, it build a tweet including the picture, the author, the location and the copyrights infos, using tweepy.
I run this script every morning with a cron job.
