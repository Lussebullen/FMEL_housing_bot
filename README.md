# FMEL Bot

This is a bot I created to search for first-come-first-served housing in Lausanne, where
the website didn't have a proper api or date filtering search function. 

It is an automated housing availability search bot.

I stopped refining this as I found housing in Stockholm and decided to attend KTH instead.

## How to run

Create a ```.env``` file with the following keys:

- FMEL_USERNAME - Username to the FMEL website
- FMEL_PASSWORD - Password to the FMEL website
- USER_KEY - Pushover user key
- APP_TOKEN - Pushover app token

After saving the file in the root directory, simply run ```main.py```, and leave it running as long as you wish for it to search for housing.

## Description of files

The program consists of 3 python scripts:

```login.py``` - 
Contains the webscraping specific to the FMEL website, all the navigation and HTML parsing etc.

```main.py``` - 
Contains the loop that runs the check in regular intervals.

```notify.py``` - 
Contains the function that sends a notification to the "pushover" application on my phone.