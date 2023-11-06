# bonappetit.com-changing-meal-checker
Simple python program that checks for meals containing certain items in bonappetit.com menus that change daily.  An example of a menu that functions well with the program are menus on bonappetit.com from universities.  The program is hardcoded to try to label the food as either: lunch, breakfast, dinner, or brunch.  If it isn't in one of these categories it won't add to the RSS feed.

If bonappetit.com changes the layout of the menu's, then the program might not work.
## Software Used
- Python 3.11
- beautifulsoup4 4.12.2
- requests 2.31.0
- rfeed 1.1.1

No guarantees that the program will work with other versions of Python or the packages.

## How To Use
1. Download "FoodFinder.py" and "FeedList.txt" into the same directory.
2. In that same directory, make a new directory called "RSSFeeds" (this is where the RSS feed files will reside)
3. Write the function "feedUrl" in "FoodFinder.py" to correctly make the links to your feeds
4. Add configuration to the "FeedList.txt" file.  The format is as follows (NOTE: any text preceded by "#" is ignored):
   
        <RSS Feed name> | <List of foods to check for> | <base url>

   Here is an example with a MIT food court and checking for Cheese Pizza and Scrambled Eggs:
   
        MITRSSFEED | ["Cheese Pizza", "Scrambled Egg"] | https://mit.cafebonappetit.com/cafe/the-howard-dining-hall-at-maseeh/

   The resulting RSS feed might look like this in your RSS feeder application:

        Cheese Pizza
            Lunch	Monday, November 6, 2023
          	Dinner	Monday, November 6, 2023
          	Lunch	Tuesday, November 7, 2023
          	Dinner	Tuesday, November 7, 2023
          	Lunch	Wednesday, November 8, 2023
          	Dinner	Wednesday, November 8, 2023
          	Lunch	Thursday, November 9, 2023
          	Dinner	Thursday, November 9, 2023
          	Lunch	Friday, November 10, 2023
          	Dinner	Friday, November 10, 2023
          	Brunch	Saturday, November 11, 2023
          	Dinner	Saturday, November 11, 2023
          	Dinner	Sunday, November 12, 2023
        Scrambled Egg
          	Breakfast	Monday, November 6, 2023
          	Breakfast	Tuesday, November 7, 2023
          	Breakfast	Wednesday, November 8, 2023
          	Breakfast	Thursday, November 9, 2023
          	Breakfast	Friday, November 10, 2023
          	Brunch	Saturday, November 11, 2023
          	Brunch	Sunday, November 12, 2023
        ERROR STATUS: NO ERRORS
