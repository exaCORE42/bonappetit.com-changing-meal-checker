import datetime
from bs4 import BeautifulSoup
import requests
from datetime import *
from rfeed import *
from ast import literal_eval


# feedName includes .xml
def feedUrl(feedName):
    # TODO: FILL IN THIS FUNCTION WITH A NAMING SCHEME THAT FITS USE CASE
    return ""


def readFeedList(feedListName):
    feedList = open(feedListName, 'r')
    feedDict = {}
    for line in feedList:
        if line[0] != "#":
            line_list = line.split(" | ")
            feedDict[line_list[0]] = {'foodList': literal_eval(line_list[1]), 'base_url': line_list[2].strip()}
    return feedDict


def menuAtDate(date, base_url):
    month, day, year = date
    date = str(year) + "-" + f"{month:02}" + "-" + f"{day:02}"
    url = base_url + date + "/"
    print(url)
    return requests.get(url).text


def findAllInstances(theList, element):
    indexList = []
    for i in range(len(theList)):
        if element == theList[i]:
            indexList.append(i)
    return indexList


# Creates a dictionary with each key being a food name, each value being a list of buttons that correspond to said key
def searchForFoodButtons(foodList, data):
    soup = BeautifulSoup(data, 'html.parser')
    list = soup.find_all('button')
    foodButtonsDict = {}
    for food in foodList:
        foodButtonsDict[food] = []
        for button in list:
            if button.text.strip() == food:
                foodButtonsDict[food].append(button)
    return foodButtonsDict


# BACKUP SYSTEM TO DETECT POSSIBLE ERRORS
# Checks the page text and creates a foodInfoDict to compare to other foodInfoDict
def searchPageText(foodList, date, data, foodInfoDict):
    date = dateToString(date)
    soup = BeautifulSoup(data, 'html.parser')
    textList = [x for x in soup.stripped_strings]
    meals = ["Lunch", "Breakfast", "Dinner", "Brunch"]
    for food in foodList:
        if food not in foodInfoDict:
            foodInfoDict[food] = []
        if food in textList:
            for index in findAllInstances(textList, food):
                i = index
                while i >= 0 and (textList[i] not in meals):
                    i -= 1
                if {"date": date, "time": textList[i]} not in foodInfoDict[food]:
                    foodInfoDict[food].append({})
                    foodInfoDict[food][-1]["date"] = date
                    foodInfoDict[food][-1]["time"] = textList[i]
    return foodInfoDict


# Converts date tuple to a string
def dateToString(tuple):
    month, day, year = tuple
    return datetime(year, month, day).strftime('%A, %B %-d, %Y')


# takes in a dictionary of buttons (from searchforfoodbuttons function), the date, and the foodInfoDict in order to
# output a new, updated foodInfoDict where each key is a food, each value is a list of dictionaries containing elements
# where each element is one date and time combo when that food is available
def searchFoodButtonsDict(dictionary, date, foodInfoDict):
    date = dateToString(date)
    for food in dictionary:
        if food not in foodInfoDict:
            foodInfoDict[food] = []
        for i in dictionary[food]:
            parents = i.parents
            # If detect 2 parents with tag type section and id of breakfast, lunch, or dinner then it could break!!!!
            for parent in parents:
                try:
                    # makes sure that it is in a section of brunch, dinner, breakfast, lunch and then makes sure it's not a duplicate
                    if parent.name == "section" and (parent.attrs['id'] in ['breakfast', 'lunch', 'dinner', 'brunch']) and ({"date": date, "time":  parent.attrs['id'].capitalize()} not in foodInfoDict[food]):
                        foodInfoDict[food].append({})
                        foodInfoDict[food][-1]["date"] = date
                        foodInfoDict[food][-1]["time"] = parent.attrs['id'].capitalize()
                except:
                    pass
    return foodInfoDict


def createFeed(foodInfoDict, errorStatus, rssName):
    description = ""
    noneTest = False
    for food in foodInfoDict:
        if len(foodInfoDict[food]) > 0:
            description += "\n" + food
            noneTest = True
        for i in foodInfoDict[food]:
            description += "\n\t" + i["time"] + "\t" + i["date"]
    description += "\n\nERROR STATUS: " + errorStatus
    if noneTest:
        # Create RSS feed
        description = "<pre>" + description + "</pre>"
        thisWeek = Item(
            title = "Food Report For the Upcoming Week",
            description = description,
            author = "Automated Menu Checking Bot",
            guid = Guid("YOURFOODREPORTFROM" + str(datetime.now())),
            pubDate = datetime.now()
        )
        myFeed = Feed(
            title = rssName,
            link = feedUrl(rssName + ".xml"),
            description = "Food Finder Instance",
            language = "en-US",
            lastBuildDate = datetime.now(),
            items = [thisWeek]
        )
        feedFile = open("RSSFeeds/" + rssName + ".xml", 'w')
        feedFile.write(myFeed.rss())


def rssCreator(rssName, foodList, menuList):
    foodInfoDict = {}
    foodInfoDictText = {}
    for date in menuList:
        currentMenu = menuList[date]
        # use button method
        foodInfoDict = searchFoodButtonsDict(searchForFoodButtons(foodList, currentMenu), date, foodInfoDict)

        # use text method
        foodInfoDictText = searchPageText(foodList, date, currentMenu, foodInfoDictText)
    # Compare 2 foodInfoDicts to check for errors
    if foodInfoDict == foodInfoDictText:
        createFeed(foodInfoDict, "NO ERRORS", rssName)
    else:
        createFeed(foodInfoDict, "ERRORS FOUND! CONTACT ADMIN.", rssName)


def main():
    feedListDict = readFeedList("FeedList.txt")

    # A week plus number of days until sunday (figure out value of variable addToSeven)
    today = datetime.now()
    addToSeven = 0
    while (today + timedelta(7 + addToSeven)).weekday() != 0:
        addToSeven += 1

    # Create Menu list.  It is a dictionary with keys being base urls and values being a dictionary with dates as keys
    # and menu HTML code as values
    menuList = {}

    for feed in feedListDict:
        if feedListDict[feed]['base_url'] not in menuList:
            menuList[feedListDict[feed]['base_url']] = {}
    for url in menuList:
        # check until NEXT sunday (at least 7 days)
        for i in range(7 + addToSeven):
            # setup date tuple
            currentDate = today + timedelta(i)
            year = currentDate.year
            month = currentDate.month
            day = currentDate.day
            # (month, day, year) format!
            date = (month, day, year)

            # currentDate menu
            menuList[url][date] = menuAtDate(date, url)
    # run feed creator for each feed
    for feed in feedListDict:
        rssCreator(feed, feedListDict[feed]['foodList'], menuList[feedListDict[feed]['base_url']])


main()
