# gfonts-sil-tracker
This project is meant to help provide analytics from [Google Font Analytics](https://fonts.google.com/analytics), which has no API.

The business side of this project resides in *tracker.py*. This utility first fetches font statistics from [Google Font Analytics](https://fonts.google.com/analytics). Then it cleans it up and filtres for fonts where SIL International is the *sole* author, then *appends* *font_metrics.csv* file just under the heading, or first row of this csv file. 

This project is set up with a Github workflow which is set up using *.github/workflows/run_tracker.yml* to spin up an ubuntu container which checks out this repository, sets up Python, installs dependencies, runs the *tracker.py* script and finally serves up an email to me which attaches the latests font_metrics.csv. Oh, yes, and the only data that is populated into the csv file is: Date (of running the script), Font name, Weekly Views, Lifetime Views.

## Future Development Angles

* This was first stab at trying to get analytics from [URL to get the Google Fonts analytics in JSON format](https://fonts.google.com/metadata/stats).

I'll consult with the rest of WSTech leadership about what the next steps to move this into the **useful** category of utilities. 
* Very likely it would be useful to have this utility *write* back the *csv* file back into the repo, i.e. add, commit, and push to the repo in order to have the font stats tabulated.
* It may prove useful to collect this data daily.
* Perhaps moving forward it might make more sense to have a different way of storing the data, such as in a database?
* It most likely would be useful to have some kind of dashboard that does font statics deltas between dates that a user selects.
* There is more information that could be gleaned, but I wasn't sure how useful it was:

```json
   "viewsByBrowser": {
      "Chrome": 0.704,
      "CriOS": 0.022,
      "Edg": 0.024,
      "Firefox": 0.018,
      "GSA": 0.012,
      "Others": 0.037,
      "Safari": 0.184
    },
    "viewsByOS": {
      "Linux": 0.362,
      "Macintosh": 0.199,* It most likely would be useful to have some kind of dashboard that does font statics deltas between dates that a user selects.
      "Others": 0.008,
      "Windows": 0.179,
      "X11": 0.036,
      "iPad": 0.007,
      "iPhone": 0.209
```

## Some notes

* The actual [URL to get the Google Fonts analytics in JSON format](https://fonts.google.com/metadata/stats) found by using developer tools (F12) on browser pointing to [Google Font Analytics Page](https://fonts.google.com/analytics)

Have "conversations" with Gemeni especially for troubleshoothing and doing the testing.

### Transparent method of developing this

* The following notes are admitedly rather basic, but I find it helpful when this is not my **day job**, to record ways I've set things up or how I've gone about developing something.

* Here is a rough go at the initial conversation to kick off the project:

> Using a TDD approach, I'd like to use Python to write a "webscraper" called "gfonts-sil-tracker" which pulls the data from wherever https://fonts.google.com/analytics assembles it. I'm only interested in the fonts with SIL International as the sole designer. I work on linux computers, so yeah a cron job seems like a good way to keep this ticking. I like the CSV approach to storing the data that is scraped. I also like the idea of updating the csv file in the github repo itself.

### These notes are just for me to remember how I set up the environment

* To get started ... set up python3 virtual environment, and install pytest and requests. And setup the gitignore file.

```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest requests
echo -e "pytest\nrequests" > requirements.txt
echo -e "venv/\n__pycache__/\n.pytest_cache/" > .gitignore
```

* Don't forget to "source venv/bin/activate" when you return to your work after shutting down or ...