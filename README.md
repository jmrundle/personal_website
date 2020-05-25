# Personal Site
 - Source files for my personal site
 - Runs on a Flask web server
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
pip install -r requirements.txt
```
#### 3. Config
- There are four config files
    - Public: 
        1. [config.py](config.py): public configuration (debug mode, api refresh rate, ... , anything that is fine to stay in git repo)
        2. [social_config.yml](social_config.yml): configures how we handle a given social media platform (shouldn't need to touch, unless you wan't to add support for another platform)
    - Private
        1. [instance/.env](instance/.env):  optional file to declare environmental variables.  Use this for API keys, access tokens, etc.
            - NOTE: this is simply an alternative to setting each env variable explicitly in the shell with: 
              ```bash
              export CONFIG_VARIABLE=value
              ```
        2. [instance/info.yml](instance/info.yml): personalized information for site
           - Stores social media usernames, resume info, etc. to personalize site
- Put all instance files (images, favicon, resume, etc) in the [instance directory](instance)
    - files in this directory won't be tracked by git, thus, it's a good place to keep personal information, images, etc.
    - The URL resource handler, [routes.py](personal_site/routes.py), checks this instance directory when loading any files not required by the application (i.e. favicon.ico, resume.pdf, etc.)

---

#### Integrating API Services
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
