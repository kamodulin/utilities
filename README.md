# Common utilities

## scrambler.py
Encode files in a directory to perform manual blind image analysis. Exports keys and a log.

## magellan.py
Simple webscraping to fetch bioRxiv and Nature Journal data. Pubmed is clearly better.

## focus.py
Block specific URLs during working hours. Only Twitter for now.

Schedule job via crontab:
```
sudo crontab -e

0 9,17 * * * /usr/bin/python3 path/to/focus.py >> out.log 2>&1
```