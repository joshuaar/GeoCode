GeoCode
=======

Command line access to google's GeoCoding service. Keeps within Google's daily limit and saves spot in address list.

##Usage
GeoCode.py uses Google's geocoding API to turn search strings (addresses) into Lat/Long coordinates.

It has a command line interface:


    GeoCode.py -j JSDUMP -l LIMIT [-s SKIP] ghlist

- ghlist: list of addresses for geocoding, one address per line.
- JSDUMP: file to dump JSON results from google. One response per line.
- LIMIT: don't make more than LIMIT API calls.
- SKIP: optional. Skip lines from the batch input in ghlist. for splitting API calls into multiple days.

##Example

Say you have a file called ghlist.txt with 100k addresses, one per line. The addresses are like text you put into the Google search bar. They don't have to follow any specific format. Google allows 2500 requests per day. You could geocode these in less than a month for free.

run:


    python GeoCode.py -j results.jsonlist -l 2500 -s .skipfile ghlist.txt

Your geocoded results will be written to results.jsonlist. The next day come back and run the command again until all addresses are geocoded.

or use cron:


    sudo crontab -e

and put this in the crontab:


    20 0 * * * python $MYGEOCODEPATH/GeoCode.py -j result.jsonlist ghcounts.txt -l 2500 -s $MYGEOCODEPATH/.skip.txt

This will run the script daily at 12:20am.

