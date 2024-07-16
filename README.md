FILES:
index.html:
this is just the html file that just starts by taking the runs in routes.js and adding them all as layers to a mapbox map. basically nothing else goes on here. 
If you want to change the thickness its in the addLayer function in the script part

get-runs-from-scratch.py:
This is a python script that will get runs from strava if you have nothing. it wll write them to routes.js. only use this the first time to make your
routes.js file. HOW IT WORKS: at the top theres per_page=X,page=Y. per_page divides your activities into clumps of that many and page sets you to
the clump Y (1 is the most recent). because of the limits of the strava api i found that you can safely use 100-125 per_page and read 1 page every 15 
minutes. thus if you have say 2000 activities, then you'd have 16 pages of 125 activities. so you would set 125 to per_page and then set page
to 16. then run the code. then 15 then run it and so forth. THE CODE IS NOT SMART so it will add duplicates so don't push the boundary of the api limit
just do 125 every 15 minutes even if it doesn't hit the limit. also the way the update code is written its important the most recent run is last so 
do page 16 first then 15 ... then 1 not the other way around. 

get-new-routes.py:
This is the only file that is actually made well. this just goes and finds the date of the last run of the file (it assumes thats the most recent)
Then it reads in your last 50 activities. (you can make this bigger or smaller by changing per_page) and then adds the ones that are later than your most
recent run. Thus even if you only have 1 run to update it just reads the last 50 which takes seconds and only adds the last run to routes.js

routes.js:
just holds an array of all the routes you have for the html file to read in and display
