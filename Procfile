web: gunicorn 'personal_site:build_app()'
release: mkdir instance/tmp && echo '\n$(heroku config:get SPOTIPY_CACHE -s)'  >> instance/tmp/.spotify-cache