# airbnb_scraper :spider:

Spider built with scrapy and ScrapySplash to crawl Airbnb and HomeAway listings of Luxembourg.
Fork of [airbnb_scraper](https://github.com/kailu3/airbnb-scraper)

## Set up

Since Airbnb uses JavaScript to render content, just scrapy on its own cannot suffice sometimes. We need to use Splash as well, which is a plugin created by the Scrapy team that integrates nicely with scrapy.

**To install Splash, we need to do several things:**
1. Install [Docker](https://docs.docker.com/install/), create a Docker account (if you don't already have one), and run Docker in the background before crawling with

```
docker run -p 8050:8050 scrapinghub/splash
```
It might take a few minutes to pull the image for the first time doing this. When this is done, you can type `localhost:8050` in your browser to check if it's working. If an interface opens up, you are good to go.

2. Install scrapy-splash using pip

```
pip install scrapy-splash
```

See [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) if you run into any issues.

## Crawling

TBD

## Acknowledgements

I would like to thank **kailu3** from whom I forked this project.
