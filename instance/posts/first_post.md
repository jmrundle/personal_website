---
title: First Post
description: Welcome to my website!
image: /resources/profile.jpeg
tags:
  - first-post
  - AWS
  - Flask
---

# Welcome
Hello!  If you're seeing this, thank you for taking a look at my website!  I've certainly learned a lot throughout the process of making this, and I've even had a bit of fun along the way.  Regardless, it's nice to have other people view the results of my labor, so thank you!

Now that you're here, let me outline a few of what I think are noteworthy tidbits regarding the site.

## Concept and Creation
My goal for this site was to create a platform to broadcast various information about myself, my projects, and maybe even my thoughts (someday).
I also wanted this platform to be easy to maintain once it was up and running.
Meanwhile, I saw this platform as a good opportunity to familiarize myself with a variety of new technologies, without completely overwhelming myself with laborious research in order to do so (it is summer break after all).


To start, I used my existing Python/Flask skills to create the basic boilerplate necessary for any website: generic source code structure, function handlers for the various URL endpoints, basic git configuration, etc.

```none
├── config
├── instance
│   ├── posts
│   ├── resources
│   ├── tmp
│   └── info.yml
├── personal_site
│   ├── static
│   │    ├── js
│   │    └── css
│   └── templates
└── scripts
```

From there, I began integrating dynamic content generation from a configuration of easily modifiable [YAML](https://pyyaml.org/wiki/PyYAML) files.  These files sit outside the core website logic, within the `/instance` directory.
The idea is that once the site is up and running, you can ignore all of the other project files and solely focus on managing these content-driving resources.

Beyond this, I also sought to introduce various forms of dynamic content to try and make my website feel a little cooler than a traditional static portfolio.
I have and always will love [Spotify's API](https://developer.spotify.com/documentation/web-api/), so that's where I started.
Spotify's API supports numerous endpoints, of which supply information about artists, tracks, and user statistics.
I went with the [top tracks & artists](https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/) endpoint, which requires an authorized OAuth token.

This, in itself, proved to be a surprisingly difficult challenge.  In summary, my website must do the following to utilize this endpoint:

<div style="text-align: center">
    <img src="/resources/authorization.png" style="width: 45vw;" />
    <p>Image from Spotify's <a href="https://developer.spotify.com/documentation/general/guides/authorization-guide/">Authorization Guide</a></p>
</div>

1. Fetch an authorization page from Spotify
2. Display this page to myself in a browser
3. Use this page to authorize the relevant scopes
4. Parse the response for a base64 encoded code
5. Use this code when asking Spotify to generate a refreshable OAuth token 
6. Use this token along with each request to the Spotify API endpoint
7. Once the token expires after 60 minutes or so, use the expired OAuth token when asking Spotify for a new one


Carrying over this functionality into deployment also introduced multiple problems.  The main problem was storing these OAuth tokens throughout the life-cycle of this web application.
One main limitation is that I couldn't use program memory to store this information, since I don't want to go through the process of authorizing the required scopes every time I restart the Flask server.
To navigate this, I used the [Spotipy API wrapper](https://spotipy.readthedocs.io/en/2.13.0/), which handles most of this logic behind the scenes by dumping and fetching info to and from a JSON cache file.  This worked perfectly until I began using [Heroku](https://www.heroku.com/python#) for deployment.
Unfortunately, Heroku uses an [ephemeral file system](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem) which is regularly replaced from a public GIT repository.  This meant I could no longer resort to Spotipy's method of using the file system to store the authorization information.
A fully-fledged database felt like an excessive solution, so I went with [AWS S3](https://aws.amazon.com/s3/), which was pretty simple to integrate.

After that, I played with the HTML/CSS/JS until I had a nice little [page](/more) to visualize basic information about my Spotify listening habits.
I then did something similar with Github's API, to display various public git information.

The last step was to add a ["blog"](/posts) of sorts to the site.  Content for this "blog" is generated from a listing of Markdown files in the `/instance/posts` directory.
To implement this, I used the `frontmatter` library to parse metadata from the post, the `markdown2` library to convert the Markdown into HTML, then the `codehilite` library to inject CSS classes into any code embedded in the HTML.


## Change to deployment
At this point, everything worked awesomely!  However, I noticed that when I would first load the site, it would took an inordinate amount of time to load, but then subsequent attempts would load almost instantaneously.

Upon some research, I found that Heroku will regularly put their free-trial servers to sleep throughout the day, to save costs.  As a result, "new" requests to an asleep server must wait for the server to wake before restarting the worker processes.

This clearly wasn't going to work.  But as a broke college student, I wasn't willing to dump whatever amount of money to keep this site running properly.  Instead, I decided to go with [AWS EC2](https://aws.amazon.com/ec2/).
Luckily, I still had almost eight months left on my [AWS Free-Tier](https://aws.amazon.com/free), which meant I could utilize a t2.micro instance for free to meet my hosting needs!

The next task was to automate the deployment to my EC2 instance.  To do this, I created a collection of [shell scripts](https://github.com/jmrundle/personal_website/tree/master/scripts), which utilize `ssh` and `scp` to refresh source files and restart the Flask server
on the remote EC2 instance.  I also set up a Nginx HTTP server to act as a reverse-proxy to this WSGI Flask server.  There are a few benefits of doing this.
First, Nginx does most of the heavy lifting in regards to forking processes, handling routes, etc.  But also, this means that I can restart my Flask server without disabling functionality to the underlying HTTP server, which greatly simplifies the shell scripts.

Finally, I used my [Github Student Developer pack](https://education.github.com/pack) to generate a free domain name at [jackrundle.me](https://jackrundle.me), and set up a crontab to auto-renew SSL certificates with [Certbot](https://certbot.eff.org) and [LetsEncrypt](https://letsencrypt.org).
