# leetcode downloader
A program to download leetcode solutions. Automatically generates a repository with timestamped commits


## How to use:
### Dependencies
Run
```
pipenv install
```
Alternatively
```
pip install requests GitPython python-dotenv
```
### Cookie String
You have to add your cookie string to `.env`

To find your cookie string, go to `leetcode.com` and log in.

Then, you can go to https://leetcode.com/api/submissions/?offset=0&lastkey= \
When you are on a page with the response, go to the network part of your browser console, and locate the cookie in the request headers 

the cookie string should start with something like `csrftoken=` 

copy the entire cookie and paste it into `.env`

`.env` should look something like this:

```.env
COOKIE_STRING=csrftoken=SOMERANDOMSTRING
...
```

### Running the program
After installing the dependencies and adding your cookie string to `settings.py`, run
```
pipenv run python main.py
```
or
```
python main.py
```

