# tweet-google-map-image
Tweeterbot to publish an image from Google map

The bot take a random Swiss commune name from a CVS file,  build from the Switzerland administration list here:
https://www.bfs.admin.ch/bfs/fr/home/statistiques/catalogues-banques-donnees/publications.assetdetail.2245010.html

It search the commune into Google map and get the photo-reference of this place
https://maps.googleapis.com/maps/api/place/textsearch/json?query=123+main+street&key=YOUR_API_KEY
Then it download the photo locally.

And finally, it build a tweet with the image, the image author name, the location name and the copyrights infos, using tweepy.
