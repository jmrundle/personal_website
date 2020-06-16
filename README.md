# Personal Site
 - Source files for a simple website template
 - Runs on a Flask web server
 - Generates content from a configuration of YML files
 - (*Will be*) deployed to an AWS EC2 instance 

---

### Running your own instance
#### 1. Setup virtual environment (recommended)
```bash
python3 -m virtualenv venv
source venv/bin/activate
```
#### 2. Download Required Files
```bash
git clone URL
cd personal_site
pip3 install -r requirements.txt
```
#### 3. Config
- There are four main config files
    - Public: 
        1. [config.py](config.py): public configuration
        2. [social_config.yml](social_config.yml): configures how we handle a given social media platform (shouldn't need to touch, unless you wan't to add support for another platform)
    - Private
        1. [instance/info.yml](instance/info.yml): information for site
           - Stores name, social media usernames, resume info, etc. to generate site content
        2. [.env](.env):  completely optional file to declare environmental variables.  Use this for API keys, access tokens, etc.
            - NOTE: this is simply an alternative to setting each env variable explicitly in the shell with: 
              ```bash
              export CONFIG_VARIABLE=value
              ```
         
- [instance directory](instance)
     - In general, the instance directory contains all the files separate from the website template itself
     - By default, the sub-folders (posts, resources, and tmp) each serve their own purpose as well
         - the [posts](instance/posts) directory contains all the markdown files for the blog, each of which contains a frontmatter with brief metadata about the post
         - the [resources](instance/resources) directory is used for images, pdf files, etc. to be referenced in [info.yml](instance/info.yml) via `/resources/<filename>`
         - the [tmp](instance/tmp) directory is used to store temporary content, such as cached API tokens
    - These path to these sub-folders can be configured in [config.py](config.py)
    - Nothing in this folder is tracked by git, although this behavior can be changed in the [.gitignore](.gitignore) by removing the following lines:
        ```gitignore
        instance/*
        !instance/*/
        !/instance/*.example
        instance/*/*
        !instance/*/.gitkeep
        ```
      - Actually, right now it is tracked by GIT, but I'll look into S3 deployment later
---

### Integrating API Services
1. Github
    - Export github username to config
        ```bash
        GITHUB_USERNAME=your_github_username
       ```
   - (*optional*) Create an [access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) with `read:user` scope (higher rate limits)
   - Export access token to config
        ```bash
        GITHUB_ACCESS_TOKEN=your_access_token
        ```
2. Spotify
    - [Register your app with Spotify](https://developer.spotify.com/dashboard/applications)
    - Add client_id, client_secret, and redirect_uri to config
        ```bash
        SPOTIFY_CLIENT_ID=your_spotify_client_id
        SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
        SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri 
        ```
   - in order to access your personal spotify data, you will have to impersonate the client in Spotify's OAuth authentication protocol
   - run setup_spotify.py to generate an access token
        ```python3
        python3 setup_spotify.py
        ```
   - this will open a browser, and prompt you for permission for the application to access the required scopes
   - after you have granted permission, a token is generated and is saved to `instance/tmp/.spotify-cache`, which is not tracked by git
   - TODO: implement system to keep this hidden from GitHub/GitLab, but include in Heroku deployment
       - database of API_Service_Name -> token -> refresh_token ?
---
### Adding Blog Posts
1. Write blog post content to Markdown files in the [posts](instance/posts) directory
2. Include metadata about each post in the file's frontmatter, which looks like the following:
    ```markdown
    ---
    title: Blog Post
    description: An amazing story
    image: /resources/image.png
    tags:
      - huge
      - important
    ---
   
    ## Post Content
    ```
