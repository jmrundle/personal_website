---
title: First Post
description: Welcome to my website!
image: /resources/profile.jpeg
tags:
  - first-post
  - website
  - Flask
---

## Welcome
Hello!  If you're seeing this, thank you for taking a look at my website!  I've certainly learned a lot throughout the process of making this, and I've even had a bit of fun along the way.  Regardless, it's nice to have other people view the results of my labor, so thank you!

Now that you're here, let me outline a few of what I think are noteworthy tidbits regarding the site.

### Concept and Creation
My goal for this site was to create a platform to broadcast various information about myself, my projects, and maybe even my thoughts (someday).
I also wanted this platform to be easy to maintain once it was up and running.
Meanwhile, I saw this platform as a good opportunity to familiarize myself with a variety of new technologies, without completely overwhelming myself with laborious research to do so (it is summer break after all).

To start, I used my existing Python/Flask skills to create the basic boilerplate necessary any website: generic source code structure, function handlers for the various URL endpoints, basic git configuration, etc.

From there, I began integrating dynamic content generation from a configuration of easily modifiable YAML files.  These files sit outside the core website logic, within the `/instance` directory.
The idea is that once the site is up and running, you can ignore all of the other project files and solely focus on managing these content-driving resources.

Beyond this, I also sought to introduce various forms of dynamic content to try and make my website feel cooler than a typical static blog (nothing against that... I just like the challenge).
I have and will always love [Spotify's API](https://developer.spotify.com/documentation/web-api/), so that's exactly where I started.
Spotify's API supports numerous endpoints, which supply information about many different artists, tracks, and user statistics.
I went with the [top tracks & artists](https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/) endpoint, which requires an authorized OAuth token.

This, in itself, proved to be a surprisingly difficult challenge.  In summary, my website must do the following to utilize this endpoint:
1. Fetch an authorization page from Spotify
2. Display this page to myself
3. Authorize the relevant scopes
4. Parse the response for a base64 encoded code
5. Use this code to ask Spotify generate a refreshable OAuth token 
6. Use this token along with each request to the Spotify API endpoint
7. Once the token expires after 60 minutes or so, use the expired OAuth token to ask Spotify for a new one

Carrying over this functionality into deployment also introduced multiple problems.  The main problem was how to store these OAuth tokens throughout the life-cycle of the website.
One main limitation is that I couldn't use program memory to store this information, since I don't want to go through the process of authorizing the required scopes every time I restart the server.
I used the Spotipy API wrapper to handle most of this logic behind the scenes, and it worked perfectly fine until I began using Heroku for deployment.
Unfortunately, Heroku uses an ephemeral file system which is regularly transferred from a public GIT repository.  This meant I could no longer resort to Spotipy's method of using the file system to store the authorization information.
A fully-fledged database felt like an excessive solution, so I went with AWS S3, which was pretty simple to integrate.

After that, I played with the HTML/CSS/JS until I had a nice little page to visualize basic information about my Spotify listening habits.
I then did something similar with Github's API, to display various public git information.

I then added a "blog" of sorts to the site, which is generated from a listing of Markdown files in the `/instance` directory.  The implementation for this was super straight forward.
I used the `frontmatter` library to parse metadata from the post, then the `markdown` library to convert the Markdown into HTML.  Next up was some syntax highlighting, and I primarily just used the `codehilite` extension to properly highlight code within the formatted HTML.


## Change to deployment
At this point, everything worked awesomely!  However, I noticed that when I would first load the site, it would took an inordinate amount of time to load, but then subsequent attempts would load almost instantaneously.

Upon some research, I found that Heroku will regularly put their free-trial servers to sleep throughout the day, to save costs.  As a result, "new" requests to an asleep server must wait for the server to first wake then reload the worker processes.

This clearly wasn't going to work.  But as a broke college student, I wasn't willing to dump whatever amount of money to keep this site running properly.  Instead, I sought out AWS EC2.
Luckily, I still had/have almost a year left on my AWS Free-Tier, which meant I could utilize a t2.micro instance for free AND meet my hosting needs!

The next task was to automate the deployment to my EC2 instance.  To do this, I created a collection of shell scripts to copy/refresh source files and restart the Flask server.
These scripts primarily use `ssh` and `scp` to do so.  I also set up a Nginx HTTP server to act as a reverse-proxy to my WSGI Flask server.  There are a few benefits to this.
First, the Nginx does most of the heavy lifting in regards to forking processes, handling routes, etc.  But also, this means that I can restart my Flask server without having to restart the Nginx HTTP server.

Finally, I used my Github Student Developer pass to generate a free domain name:  [jackrundle.me](http://jackrundle.me).

And that's all she wrote (for now).