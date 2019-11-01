# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import JSONRequest
from homeaway_scraper.items import HomeawayScraperItem
from scrapy.exceptions import CloseSpider
import json


class HomeawaySpider(scrapy.Spider):
    name = 'homeaway'
    allowed_domains = ['homeaway.com']
    start_urls = ['http://homeaway.com/']
    post_data = '''
    {{
        "operationName":"SearchQuery",
        "variables":{{
        "params":{{
            "adultsCount":1,
            "filter":[
    
            ],
            "maxBathrooms":null,
            "maxBedrooms":null,
            "maxPrice":null,
            "minBathrooms":0,
            "minBedrooms":0,
            "minPrice":0,
            "page":{page},
            "petIncluded":false,
            "q":"{keyword}",
            "include":[
                "percentBooked"
            ]
        }},
        "url":"/search/keywords:{keyword}"
        }},
        "extensions":{{
        "isPageLoadSearch":true
        }},
        "query":"query SearchQuery($params: ResultsParams, $url: String) {{  results(params: $params) {{    headlineTitle    internal {{      searchServiceUrl      __typename    }}    liveRegionRedirectUrl    pidRedirectUrl    id    typeaheadSuggestion {{      uuid      term      name      __typename    }}    geography {{      lbsId      location {{        latitude        longitude        __typename      }}      isGeocoded      shouldShowMapCentralPin      __typename    }}    ...BreadcrumbResults    ...ExpandedGroupsResults    ...PagerResults    ...DestinationMessageResults    ...FilterCountsResults    ...HitCollectionResults    ...HtmlTitleResults    ...ADLResults    ...MapResults    ...SearchTermCarouselResults    ...SeoContentResults    ...InternalToolsResults    __typename  }}  ...RequestMarkerFragment}}fragment BreadcrumbResults on Results {{  destination {{    breadcrumbs {{      name      url      __typename    }}    __typename  }}  __typename}}fragment HitCollectionResults on Results {{  page  pageSize  listings {{    ...HitListing    __typename  }}  pinnedListing {{    listing {{      availableForDates      ...HitListing      __typename    }}    __typename  }}  __typename}}fragment HitListing on Listing {{  virtualTourBadge {{    name    id    helpText    __typename  }}  amenitiesBadges {{    name    id    helpText    __typename  }}  multiUnitProperty  imageCount  images {{    altText    c6_uri    c9_uri    __typename  }}  listingNamespace  ...HitInfoListing  __typename}}fragment HitInfoListing on Listing {{  ...DetailsListing  ...PriceListing  ...RatingListing  ...GeoDistanceListing  detailPageUrl  instantBookable  minStayRange {{    minStayHigh    minStayLow    __typename  }}  listingId  partnerBadges {{    id    helpText    name    __typename  }}  rankedBadges(rankingStrategy: SERP) {{    id    helpText    name    __typename  }}  propertyId  listingNumber  propertyType  propertyMetadata {{    headline    propertyName    __typename  }}  reviewBadges {{    id    name    helpText    __typename  }}  unitMessage(assetVersion: 1) {{    iconText {{      message      icon      messageValueType      __typename    }}    __typename  }}  __typename}}fragment DetailsListing on Listing {{  bathrooms {{    full    half    toiletOnly    __typename  }}  bedrooms  propertyType  sleeps  petsAllowed  spaces {{    spacesSummary {{      area {{        areaValue        __typename      }}      __typename    }}    __typename  }}  __typename}}fragment PriceListing on Listing {{  averagePrice {{    currencyUnits    periodType    value    __typename  }}  totalPrice {{    currencyUnits    periodType    value    __typename  }}  priceSummary {{    edapEventJson    formattedAmount    pricePeriodDescription    __typename  }}  __typename}}fragment RatingListing on Listing {{  averageRating  reviewCount  __typename}}fragment GeoDistanceListing on Listing {{  geoDistance {{    text    __typename  }}  __typename}}fragment ExpandedGroupsResults on Results {{  expandedGroups {{    ...ExpandedGroupExpandedGroup    __typename  }}  __typename}}fragment ExpandedGroupExpandedGroup on ExpandedGroup {{  listings {{    ...HitListing    ...MapHitListing    __typename  }}  mapViewport {{    neLat    neLong    swLat    swLong    __typename  }}  __typename}}fragment MapHitListing on Listing {{  ...HitListing  geoCode {{    latitude    longitude    __typename  }}  __typename}}fragment FilterCountsResults on Results {{  id  resultCount  filterGroups {{    groupInfo {{      name      id      __typename    }}    filters {{      count      checked      filter {{        id        name        refineByQueryArgument        description        __typename      }}      __typename    }}    __typename  }}  __typename}}fragment MapResults on Results {{  mapViewport {{    neLat    neLong    swLat    swLong    __typename  }}  page  pageSize  listings {{    ...MapHitListing    __typename  }}  pinnedListing {{    listing {{      ...MapHitListing      __typename    }}    __typename  }}  __typename}}fragment PagerResults on Results {{  fromRecord  toRecord  pageSize  pageCount  page  resultCount  __typename}}fragment HtmlTitleResults on Results {{  pageTitle  metaDescription  metaKeywords  canonicalLink(url: $url)  alternativeLinks(url: $url) {{    link    hrefLang    __typename  }}  __typename}}fragment DestinationMessageResults on Results {{  destinationMessage(assetVersion: 1) {{    iconTitleText {{      title      message      icon      messageValueType      __typename    }}    iconText {{      message      icon      messageValueType      __typename    }}    __typename  }}  __typename}}fragment ADLResults on Results {{  parsedParams {{    q    coreFilters {{      adults      children      pets      minBedrooms      maxBedrooms      minBathrooms      maxBathrooms      minPrice      maxPrice      minSleeps      __typename    }}    dates {{      arrivalDate      departureDate      __typename    }}    sort    __typename  }}  page  pageSize  pageCount  resultCount  fromRecord  toRecord  pinnedListing {{    listing {{      listingId      __typename    }}    __typename  }}  listings {{    listingId    __typename  }}  filterGroups {{    filters {{      checked      filter {{        groupId        id        __typename      }}      __typename    }}    __typename  }}  geography {{    lbsId    name    description    location {{      latitude      longitude      __typename    }}    primaryGeoType    breadcrumbs {{      name      countryCode      location {{        latitude        longitude        __typename      }}      primaryGeoType      __typename    }}    __typename  }}  __typename}}fragment RequestMarkerFragment on Query {{  requestmarker  __typename}}fragment SearchTermCarouselResults on Results {{  discoveryXploreFeeds {{    results {{      id      title      items {{        ... on SearchDiscoveryFeedItem {{          type          imageHref          place {{            uuid            name {{              full              simple              __typename            }}            __typename          }}          __typename        }}        __typename      }}      __typename    }}    __typename  }}  typeaheadSuggestion {{    name    __typename  }}  __typename}}fragment SeoContentResults on Results {{  searchReviewsHeadline  topRecentReviews {{    ...SearchReviewsTopRecentReviewSummary    __typename  }}  __typename}}fragment SearchReviewsTopRecentReviewSummary on TopRecentReviewSummary {{  listingDetails {{    listingId    thumbnailUrl    detailPageUrl    __typename  }}  review {{    title    text    createdAt    arrivalDate    rating    __typename  }}  __typename}}fragment InternalToolsResults on Results {{  internalTools: internal {{    searchServiceUrl    __typename  }}  __typename}}"
    }}
    '''

    def __init__(self, keywords='', *args,**kwargs):
        super(HomeawaySpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        self.post_data = HomeawaySpider.post_data.format(page = 1, keyword = 'luxembourg')
        self.json_post_data = json.loads(self.post_data)
        self.url = ('https://www.homeaway.com/serp/g')

    def start_requests(self):
                
        # TBD: Init param keyword should be inserted in post_data like in url.format
        # post_data = post_data.format(self.keywords)                
        yield JSONRequest(url=self.url, callback=self.parse, data=self.json_post_data)

    def parse(self, response):
        url = ('https://www.homeaway.com/serp/g')
        data = json.loads(response.body)

        # Debugging response
        ## Write response to file
        """ filename = 'ha-debug.json'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename) """

        # Return a list of all homes
        homes = data.get('data').get('results').get('listings')

        listing = HomeawayScraperItem()

        if homes is None:
            raise CloseSpider("No homes available")

        for home in homes:
            listing['listingId'] = home.get('listingId')
            listing['propertyType'] = home.get('propertyType')
            yield listing

        page = data.get('data').get('results').get('page')
        pageCount = data.get('data').get('results').get('pageCount')

        post_data = HomeawaySpider.post_data.format(page = page + 1, keyword = 'luxembourg')
        json_post_data = json.loads(post_data)
        if page <= pageCount:
            yield JSONRequest(url=url, callback=self.parse, data=json_post_data)
            print ("page = ", page)
            print ("PageCount = ", pageCount)