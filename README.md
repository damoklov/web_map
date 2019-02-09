# web_map   :honeybee:
Python application for creating HTML maps using _folium_ and _geopy_.

## Information  :dog:
###### Purpose
This application was created to build maps in _HTML_ format with data from plain text file (__docs/locations.list__).
User is asked to enter the year that he\she is interested in, and then will be given a map to be opened in web browser.

###### General structure:
1. __main.py__ -- Main application runable file.
2. __setup.py__ -- File made for installing all necessary dependencies.
3. __requirements.txt__ -- File with all necessary python packages.
4. __world.json__ -- File with information about countries (Area, Population, etc.)
5. __README.md and LICENSE.txt__ -- Files with descriptive information.
6. __docs__ -- Folder with necessary data files.
7. __maps__ -- Folder with example maps and where all further maps will be stored in.
8. __screenshots__ -- Folder with main screenshots.
9. __tests__ -- Folder with unnecessary testing samples.

###### Application Usage:
1. Clone or download _web\_map_ project.
2. Make sure that you downloaded ___all___ folders!
3. Install all packages listed in _reqiurements.txt_ file.
4. Run application: `python main.py`.
5. Follow instructions on the screen.
6. If you want application to create CSV files again, change code manually as shown here:

![S7](/screenshots/screenshot_7.png)

7. If you want to locate CSV files on your own, change code manually as shown here:

![S8](/screenshots/screenshot_8.png)

8. Enter year when asked.

Additional screenshot of working process #1:

![S1](/screenshots/screenshot_1.png)

Additional screenshot of working process #2:

![S2](/screenshots/screenshot_2.png)

## HTML structure  :panda_face:
###### List of most common tags in map document:
- \<!DOCTYPE html\> -- Defines type of a document.
- \<body\> -- Separates the body-part of a document.
- \<div\> -- Sets separate partition of a document.
- \<html\> -- Contains all the data from webmap.
- \<link\> -- Establishes the connection with external document or webpage.
- \<meta\> -- Defines metatags which store tech information for web browsers and searching engines.
- \<script\> -- Describes the script itself. Contains links to other apps.
- \<style\> -- Defines webmap style.
- \<title\> -- Defines heading of a webmap.
- \<head\> -- Separates the head-part (name) of a webmap.
###### Most common structures:
1. Structure with object and its attributes:

![S3](/screenshots/screenshot_3.png)

- __var__ -- Defines variable and sets a name for it.
- __.tileLayer__ -- Defines type of tile for a webmap.
- __attribute=...__ -- Sets some values to each attribute ("maxZoom", "tms", etc.).
- __.addTo__ -- Defines which map to add info to.
2. Scripts with JS and CSS files:

![S4](/screenshots/screenshot_4.png)

- __src=...__ -- Specifies a link to JavaScript file from outer scope.
- __rel=...__ -- Specifies the relationship between the current document and the linked document/resource.
- __href=...__ -- Specifies a link to an external CSS stylesheet file.
3. Coordinates block:

![S5](/screenshots/screenshot_5.png)

- __.geoJson__ -- States that the further data is connected with _geopy_ package.
- __[_\<latitude\>, \<longitude\>_]__ -- Coordinates for each place that will be sticked on a map.
## Summary  :octopus:
###### Layers
The map itself is generated with 3 layers of information with markers and 3 layers of different background tiles.
The first layer shows all movies independently from user's choice of the year sorted by countries.
The second layer shows all movies depending on user's choice of the year.
The third layer shows area of each country on our globe.
###### Gathered information
1. Movies started to be listed from approximately 1873 year.
2. Some years are not available in database.
3. Ukraine seems to be quite a 'filming country' as for 2013 year (63 movies filmed).
4. Ukraine's contribution to world's cinematography is 1458 movies.
5. Soviet Union's coordinates seem to be near Kiev ...
6. 71 movies were filmed in Atlantic Ocean.
7. Lots of movies seem to be created in non-ground areas such as seas, oceans or even glaciers!
8. USA is a leader in cinematography with approximately 351984 filmed of all time.

> "Lord, I pray not for a lighter load but for stronger shoulders." - St. Augustine
