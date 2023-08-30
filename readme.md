# PaladinsRankedStats
Discord of original developer (until they deleted themselves from the internet) - Aevann#6346
This version is severely outdated, but it's the only one we have now. The last original update was made during May of 2022, then we lost everything. Kinda sad
[This is how it looked before](https://docs.google.com/spreadsheets/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/), [This is how it looks now](https://docs.google.com/spreadsheets/d/1qMKyAfMxCVvfGifPjE2v-ry8_oFmSpVHSJjqdAic1uI/)
# No updates are going to be done unless told otherwise.
---
\
If you want to work on that thing hovewer here's a possible TODO list:
* create a config file
* transition from JSON to SQL (since JSON tends to break when there are files bigger than it's ego)
* use proper functions for repeating code (maybe from numpy)
* [DONE] optimize google sheet calls so that it doesn't have to use 3 accounts with 3 different API keys (it actually doesn't use these anymore)
* rewrite everything from scratch (even better)
* [DONE] remove controller version since hi-rez [removed controller queue](https://paladins.fandom.com/wiki/Paladins_Version_6.3.5218.1#Ranked:_Cross-Play,_Reset,_and_Split)
    * it also doesn't work because of Aevann1's implementation so controllergooglesheet is always empty
* implement actual ratelimiting (for both gspread and requests to paladins api)
* account for .csv fields for having commas. Right now Omen's card "More, More, More!" displays incorrectly
---
# Installation
0. Git clone
1. `pip install -r requirements.txt`
2. Create a project in [Google Cloud](https://console.cloud.google.com/)
3. Make a service key and put .json as `sheetsapikey1.json` next to .py file
4. Enable Spreadsheet API for your project
5. [Get yourself a developer key at Hi-Rez](https://fs12.formsite.com/HiRez/form48/secure_index.html)
6. Wait. It takes a few days
7. While you wait you can make a new spreadsheet. Don't forget to give full access to anyone who might see it
8. Fill the start of `PaladinsRankedStats.py` file with your data. You can set `controllergooglesheetid` to your PC link, it's not going to be filled anyways. It is required to be filled though
9. Set `firstday` to the start of this month. Not sure why though
10. Make sure it's not anywhere between 0-2AM right now. Yes, this somehow matters
11. Start `PaladinsRankedStats.py`. You're done