# leetcode downloader
A program to download leetcode solutions. Automatically generates a repository with timestamped commits


## How to use:
### Dependencies
Run
```
pip install -r requirements.txt
```
### Cookie String
You have to add your cookie string to `settings.py`

To find your cookie string, go to `leetcode.com` and log in.

Then, you can go to https://leetcode.com/api/submissions/?offset=0&lastkey= \
When you are on a page with the response, go to the network part of your browser console, and locate the cookie in the request headers 

the cookie string should start with something like `csrftoken=` 

copy the entire cookie and paste it into `settings.py`

`settings.py` should look something like this:

```settings.py
# MUST BE PROVIDED
cookie_string='csrftoken=XXXXXXXXXX'
...
```

### Running the program
After installing the dependencies and adding your cookie string to `settings.py`, run

```
python main.py
```
