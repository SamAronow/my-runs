FILES:
index.html:
this is just the html file that just starts by taking the runs in routes.js and adding them all as layers to a mapbox map. basically nothing else goes on here. 
If you want to change the thickness its in the addLayer function in the script part

get-all-runs.py:
This is a python script that will get runs from strava if you have nothing. it wll write them to routes.js. only use this the first time to make your routes.js file. HOW IT WORKS: at the top theres per_page=X,page=Y. per_page divides your activities into clumps of that many and page sets you to the clump Y (1 is the most recent). because of the limits of the strava api i found that you can safely use 100-125 per_page and read 1 page every 15 minutes. thus if you have say 2000 activities, then you'd have 16 pages of 125 activities. THE CODE WILL
NEED YOU TO MAKE ONE CHANGE: right now it has num_pages set to 8 becuase that's what I used since i have 960 pages so 8 pages of 125. if you have 16 pages like described above then change num_pages to 16 then run the code. The code will need to be on the background for 15 minutes * the number of pages. This is because the strava api can only handle a certain number of requests every 15 minutes. Thus if you have 16 pages. It also has a daily limit so you might have to split this into 2 days. It really sucks but i'm not paying for more strava api and it works enough so leaving it be. if you have more than 10 pages of 125 then you might need to split it into 2 days. (NOTE that the limit recents every day at 8pm eastern and the 15 minute limits are based off the intervals 11:00-11:15 and so forth so if you submit requests at 11:14 you can submit more at 11:15 but then you have to wait to 11:30 after that.)

get-new-routes.py:
This is the only file that is actually made well. this just goes and finds the date of the last run of the file (it assumes thats the most recent)
Then it reads in your last 50 activities. (you can make this bigger or smaller by changing per_page) and then adds the ones that are later than your most
recent run. Thus even if you only have 1 run to update it just reads the last 50 which takes seconds and only adds the last run to routes.js

routes.js:
just holds an array of all the routes you have for the html file to read in and display
