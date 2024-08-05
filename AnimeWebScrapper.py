# -*- coding: utf-8 -*-
"""AnimeWebScrapper.pynb

Libraries to be installed:

  pip install beautifulsoup4;

  pip install IMDbPY

  pip install -U rottentomatoes-python

  pip install praw

  pip install -U mal-api
"""
import requests
import json
from requests.auth import HTTPBasicAuth
#myAnimeList
from mal import AnimeSearch
from bs4 import BeautifulSoup
#reddit
import praw
from praw.models import MoreComments

#getting review
import rottentomatoes as rt
import imdb

class AnimeScrapper:
  def __init__(self, animeName):
    print("init")
    self.animeName = animeName

  #letterBox is only for movies
  def getLetterBoxDairy(self,UserId):
    URL = "https://letterboxd.com/{}/films/diary".format(UserId)
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    rows=soup.find("table").find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        print(cells[2].get_text())
        print(cells[4].get_text())

  def IMDB_Review(self):
    imdbObj = imdb.IMDb()
    reltResults = imdbObj.search_movie(self.animeName)
    #print(reltResults[0].keys())
    #print(reltResults[0].values())
    for i in range(len(reltResults)):
        currentSearch=reltResults[i]
        if currentSearch['kind']=="tv series":
            print(currentSearch['title'] + " : " + currentSearch.movieID)
            searchDetails=imdbObj.get_movie(currentSearch.movieID)
            #print("Rating:",searchDetails['rating'])
            #print(searchDetails['synopsis'])

  def Rotten_Review():
    getUrl="https://rotten-tomatoes-api.ue.r.appspot.com/search/"
    rottenSearches = requests.get(getUrl+name)
    print(rottenSearches.content)

  def myAnimelist(self):
    print("anime");
    search = AnimeSearch(self.animeName);
    auth = HTTPBasicAuth("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
    p=1;
    animeListUrl=search.results[0].url+"/reviews?sort=suggested&filter_check=&filter_hide=&preliminary=on&p=";
    while(True):
      updateUrl=animeListUrl+str(p);
      print(updateUrl)
      rsp = requests.request("get",updateUrl, headers=None, auth=auth)
      soup = BeautifulSoup(rsp.content, 'html5lib')
      comments = soup.body.find_all('div', attrs={'class' : 'js-review-element'})
      for eachComment in comments:
        print(eachComment.find('a', attrs={'data-ga-click-type' : 'review-anime-reviewer'}).get_text())
        print(eachComment.find('div', attrs={'class' : 'text'}).get_text())
      if(soup.body.find('a', attrs={'data-ga-click-type' : 'review-more-reviews'})):
        print("found more reviews")
        p+=1
      else:
        break

  def redditScrapper(self):
    reddit = praw.Reddit(client_id="xxxxxxxxxxxxxxxxxxxxxxx",         # your client id
                               client_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",      # your client secret
                               user_agent="xxxxxxxxxxxxxxxxxxxxxx")        # your user agent

    for submission in reddit.subreddit("all").search(self.animeName):
        print('\033[1m' +submission.title)
        url = "https://www.reddit.com"+submission.permalink;
        submission = reddit.submission(url=url)
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            print(top_level_comment.body)

p1 = AnimeScrapper("demon slayer")
#p1.getLetterBoxDairy("xxxxxx")
#p1.myAnimelist()
p1.redditScrapper()

