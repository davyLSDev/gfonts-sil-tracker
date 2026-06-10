# gfonts-sil-tracker
This project is meant to help provide analytics from https://fonts.google.com/analytics, which has no API

Using a TDD approach, I'd like to use Python to write a "webscraper" called "gfonts-sil-tracker" which pulls the data from wherever https://fonts.google.com/analytics assembles it. I'm only interested in the fonts with SIL International as the sole designer. I work on linux computers, so yeah a cron job seems like a good way to keep this ticking. I like the CSV approach to storing the data that is scraped. I also like the idea of updating the csv file in the github repo itself.

## Some notes

To get started ... set up python3 virtual environment, and install pytest and requests. And setup the gitignore file.

```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest requests
echo -e "pytest\nrequests" > requirements.txt
echo -e "venv/\n__pycache__/\n.pytest_cache/" > .gitignore
```

Don't forget to "source venv/bin/activate" when you return to your work after shutting down or ...

The actual URL is https://fonts.google.com/metadata/stats found by using developer tools (F12) on browser pointing to https://fonts.google.com/analytics
