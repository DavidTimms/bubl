bubl: Smart Photo Sharing
===
bubl is a site for collecting, rating and sharing images based on topics. 
The site was built in Python to run on the [Google App Engine](https://developers.google.com/appengine) 
platform as a service.

The site is available at [bubl-app.appspot.com](http://bubl-app.appspot.com/), and you can view an 
[example topic page for the band Radiohead](http://bubl-app.appspot.com/radiohead). 

The concept is similar to popular social news sites like [reddit](http://reddit.com) and 
[Hacker News](http://news.ycombinator.com) - users upload images and then vote the images up or down 
to sort the best, most relevant content from the worst. The most highly rated images are displayed 
large at the top of the page, whereas low ranking images appear as thumbnails at the bottom. 

The site was built as an experiment in using Google App Engine, and uses Google's NoSQL datastore. It 
was implemented in Python using the [webapp2 framework](http://webapp-improved.appspot.com/), with 
a bit of JavaScript for validation, animation and ajax on the front-end.