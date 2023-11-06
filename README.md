# bonappetit.com-changing-meal-checker
Simple python program that checks for meals containing certain items in bonappetit.com menus that change daily.  An example of a menu that functions well with the program are menus on bonappetit.com from universities.  The program is hardcoded to try to label the food as either: lunch, breakfast, dinner, or brunch.  If it isn't in one of these categories it won't add to the RSS feed.

## To Use
1. Download "FoodFinder.py" and "FeedList.txt" into the same directory.
2. In that same directory, make a new directory called "RSSFeeds" (this is where the RSS feed files will reside)
3. Write the function "feedUrl" in "FoodFinder.py" to correctly make the links to your feeds
