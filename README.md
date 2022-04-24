# routing111
record some problems met

Problem 1: Difficult to install geopandas package on Heroku.(it needs too much dependency)
Solution: use aptfile, then add 2 buildpacks :1. https://github.com/heroku/heroku-buildpack-apt, and default python buildpack..
heroku buildpacks:clear
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python

For details: https://github.com/indielyt/heroku_dash_gdal_test


Problem 2: file path problem.
On heroku "/" and "\" are different, they cause errors, cannot find the files, dirctory...

Problem 3: duplicate problems
must git commit -am "comments", new things to heroku application, and then git push heroku master
unless it may have errors
