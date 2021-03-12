# RiggedMM
The files I used to investigate whether the cards in your opponent's deck are dependent on the cards in your deck.  (Determining analytically if matchmaking is rigged)

The purpose of this repository is to show the code I used to investigate Clash Royale ladder matchmaking.  The investigation started with u/Way2GoFromHere's comment "Why is it that I see ALL mega knights/pekkas and so put an inferno dragon in and suddenly don't see them anymore?".  My methodology here was to determine if the cards in your deck are independent of the cards in your opponent's deck.  Once I had that, I could use the chi-square test for independence to determine if the two variables were independent.  

On the technical side, there are 5 files here: excel.xlsx, battletags.txt, CVCdict.txt, emptyDict.txt and lastly riggedMM.py. The .txt files were for storing data as I conducted this investigation and the excel file was for quickly exporting my data from python.  All 5 are imperative for being able to recreate my tests.  I created a recursive tree to gather a large number of battles and then sorted the data on the decks into the corresponding spots in the dictionaries.  After running that for multiple times (n=4) or once (n=5) to get enough battles, I analyzes the data and exported it into excel. When doing different trophy ranges, I did use the function clearTags() when moving to a different range to speed up my code. 

By uploading my code to github, I'm first showing the code I used to conduct this investigation and second, I'm hoping that someone can build off my code to make other investigations into matchmaking, whether it be in Clan wars and below 4k bots. I hope this example of CR api code in python can inspire others to begin investigating the game too. 
If you do use it, please just mention me once. 

How to use this repository for other investigations into matchmaking:
1. Download all the files to the same directory
2. Download python from python.org and VS code from code.visualstudio.com (Both are free)
3. Open VS code and start a ipython terminal
3B. It is good practice to look over any code you download before running it.
4. Go to developer.clashroyale.com and make yourself an account and developer key. 
5. substitute your key in for my key on 12
6. Run riggedMM.py in the terminal
7. run the function clearTags() before starting to increase algorithm speed. 
8. Pick a starting range of trophies to be analyzed and the starter
9. type this into the terminal: data = getData(lowerBound, upperBound, startingTag, createCVCdict()) with lowerBound, upperBound and startingTags being variables you define. 
10. Repeat this until you get enough data. The last input of the the function getData should be data for subsequent runs as the data will get updated if you add the additional parameter. 
11. Writing the data to excel will overwrite what is already in the document.  I recommend moving it to a different spreadsheet or a google sheet. 
