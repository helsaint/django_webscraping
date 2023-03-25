# django_webscraping
A very simple webscraper to get a single page from transfermarket site and use it as an api input for a REACT site.
It only scrapes the first page. Extending to scrape the other pages shouldn't be that difficult but I only needed the first.
The code uses Beautiful soup and will therefore only work on sites where the data to be scraped exists in view-source.
May comeback in the future and change it to use headless-browser.
Rudimentary error detection exists
