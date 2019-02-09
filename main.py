import string
import folium
import time
import pandas
import re
import pathlib
from tqdm import tqdm
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def choose_file_location(default=True):
	"""
	Created for user's choice of directory.

	None -> list

	Usage: (suggested)
	> choose_file_location()
	"""
	choice = ['docs/locations.list',
			  'docs/locations.csv',
			  'docs/info.csv',
			  'docs/countries.csv']
	if default:
		return choice
	else:
		while True:
			choice[0] = input('Source (<locations.list>) location:')
			choice[1] = input('Dir and name of CSV file#1:')
			choice[2] = input('Dir and name of CSV file#2:')
			choice[3] = input('Dir and name of CSV file#3:')
			confirmation = input('Press Enter if you are sure ..')
			if '' in choice:
				print('Reenter locations and names of files!')
				continue
			elif confirmation == str():
				return choice

			else:
				continue

def read_user_input():
	"""
    Reads user input (year) and checks it.

    None -> int

    Usage:
    > read_user_input()
    """
	while True:
		user_year = input('Enter year (from 1873 to 2024):')
		try:
			user_year = int(user_year)
		except ValueError:
			print('Enter a valid number.')
			continue
		if 2024 >= user_year >= 1873:
			break
		else:
			print("Enter year correctly.")
			continue
	return user_year


def get_places_from_file(list_filename, csv_filename):
	"""
    Reads content of <list_filename> and writes converted data into
    <csv_filename> file.

    (str, str) -> None

    Usage: (suggested)
    > get_places_from_file('locations.list', 'locations.csv')
    """
	try:
		f = open(list_filename, 'r', encoding='utf-8', errors='ignore')
		g = open(csv_filename, 'w', encoding='utf-8', errors='ignore')
	except FileNotFoundError as err:
		print(err)
		quit()

	line = str()
	g.write('Title,Year,Location\n')  # Create headings for .csv file

	while '==============' not in line:  # Pass unnecessary lines in file
		line = f.readline()

	data = (line for line in f)
	set_of_places = set()

	print('Parsing has started ..')

	for line in data:
		newline = line.strip().split('\t')
		newline = [x for x in newline if x != '']

		# Parsing the lines
		if '(' in newline[0] and \
				newline[0][newline[0].index('(') + 1] in string.digits \
				and newline[0][newline[0].index('(') + 2] in string.digits \
				and newline[0][newline[0].index('(') + 3] in string.digits \
				and newline[0][newline[0].index('(') + 4] in string.digits:

			bracket_start = newline[0].index('(')
			title = newline[0][:bracket_start]
			title = title.replace(',', ' ') if ',' in title else title
			year = newline[0][bracket_start + 1:bracket_start + 5]
			location = newline[1].replace(',', '  ')
		else:
			continue
		set_of_places.add(str(title + ',' + year + ',' + location + '\n'))

	print('Parsing has finished ..')

	for item in set_of_places:
		g.write(item)
	f.close()
	g.close()
	print('Finished writing into {} ..'.format(csv_filename))


def find_coordinates(filename, filename2, filename3):
	"""
    Reads <filename> file and writes converted data into
    <filename2> and <filename3> files.

    (str, str, str) -> None

    Usage: (suggested)
    > find_coordinates('docs/locations.csv', 'docs/info.csv', 'docs/countries.csv')
    """
	start = time.time()
	try:
		f = open(filename, 'r', encoding='utf-8', errors='ignore')
		g = open(filename2, 'w', encoding='utf-8', errors='ignore')
		h = open(filename3, 'w', encoding='utf-8', errors='ignore')
	except FileNotFoundError as err:
		print(err)
		quit()

	f.readline()  # Read unnecessary heading line

	total_set = set()  # Creating set with title, year and place of movie
	locations_dict = dict()  # Dictionary of coordinates and their quantity

	data = (line for line in f)
	geolocator = Nominatim(user_agent='MovieMapApp', timeout=None)
	geocode = RateLimiter(geolocator.geocode,
						  min_delay_seconds=1,
						  max_retries=5)

	print('Parsing has started ..')  # Parsing data to leave only countries
	for line in data:
		place = line.strip().split(',')[-1].replace('  ', ', ').split(',')[
			-1].strip()
		year = line.strip().split(',')[-2].strip()
		title = line.strip().split(',')[0].strip()
		total_set.add((title, year, place))

		if place not in locations_dict.keys():
			locations_dict[place] = 1
		else:
			locations_dict[place] += 1

	print('Parsing has ended ..')

	coordinates_dict = dict()  # Dictionary of coordinates and their quantity
	h.write('Place,Movies,Latitude,Longitude\n')  # Headings for file

	print('Searching coordinates for locations ..')

	for key, value in tqdm(locations_dict.items()):
		location = geolocator.geocode(key)
		if location:
			coordinates = [location.latitude, location.longitude]
		else:
			location = 'N/A'
			continue
		coordinates_dict[key] = coordinates
		h.write(key + ',' + str(value) + ',' + str(coordinates[0]) + ',' +
				str(coordinates[1]) + '\n')

	print('Search has ended ..')

	g.write('Title,Year,Place,Latitude,Longitude\n')  # Headings for file
	for group in total_set:
		if group[2] in coordinates_dict.keys():
			g.write(group[0] + ',' + group[1] + ',' + group[2] + ',' +
					str(coordinates_dict[group[2]][0]) + ',' +
					str(coordinates_dict[group[2]][1]) + '\n')
		else:
			g.write(group[0] + ',' + group[1] + ',' +
					group[2] + ',' + 'N/A' + '\n')

	f.close()
	g.close()
	h.close()

	end = time.time()
	elapsed_time = end - start
	print('It took {} minutes ..'.format(str(elapsed_time / 60)))  # Sum time


def build_map(filename, filename2, user_year):
	"""
    Creates an <html> file based on <filename> and <filename2> data.
    Comfortably uses Pandas package.

    (str, str, int) -> None

    Usage: (suggested)
    > build_map('docs/info.csv', 'docs/countries.csv', year: int)
    """
	try:
		data = pandas.read_csv(filename, error_bad_lines=False)
		data2 = pandas.read_csv(filename2, error_bad_lines=False)
	except FileNotFoundError as err:
		print(err)
		quit()

	lat = data['Latitude']
	lon = data['Longitude']
	title = data['Title']
	place = data['Place']
	year = data['Year']

	lat2 = data2['Latitude']
	lon2 = data2['Longitude']
	place2 = data2['Place']
	quantity = data2['Movies']

	map_data = folium.Map(tiles='Mapbox Bright', zoom_start=13)
	fg_all_movies = folium.FeatureGroup(name='All Movies')
	fg_year_movie = folium.FeatureGroup(
						name='Movies of {} year'.format(str(user_year)))
	fg_pp = folium.FeatureGroup(name='Area')

	def color_creator(films):
		"""
        Decides which color to create for specific number.

        (int) -> str

        >>> color_creator(210)
        'yellow'
        >>> color_creator(0)
        'green'
        >>> color_creator(1000)
        'red'
        """
		if films < 100:
			return 'green'
		if 100 <= films <= 500:
			return 'yellow'
		else:
			return 'red'

	country_year_dict = dict()  # Dictionary of certain year's movies
	country_all_dict = dict()  # Dictionary of all countries' movies
	country_coordinates = dict()  # Dictionary of countries' coordinates
	print('Dictionary looping has started ..')

	for lt, ln, plc, mvs in zip(lat2, lon2, place2, quantity):
		if (lt, ln) not in country_all_dict.keys():
			country_all_dict[(lt, ln)] = mvs
		else:
			country_all_dict[(lt, ln)] += mvs
		country_coordinates[(lt, ln)] = plc

	for lt2, ln2, yr in zip(lat, lon, year):
		if yr == user_year:
			if (lt2, ln2) not in country_year_dict.keys():
				country_year_dict[(lt2, ln2)] = 1
			else:
				country_year_dict[(lt2, ln2)] += 1

	print('Map building has started ..')

	for key, item in country_year_dict.items():
		try:
			fg_year_movie.add_child(
				folium.CircleMarker(
					location=list(key),
					radius=8,
					popup=str(item) + ', ' +
						  re.sub(r'\]|\[|\.|\)|\(',  # Clear unnecessary stuff
								 '',
								 country_coordinates[key].upper())
									if key in country_coordinates else 'N/A',
					fill_color='blue',
					color='red',
					fill_opacity=0.4,
					tooltip='Press here'))
		except ValueError:
			continue

	for key, item in country_all_dict.items():
		try:
			fg_all_movies.add_child(
				folium.CircleMarker(
					location=list(key),
					radius=5,
					popup=str(item) + ', ' +
						re.sub(r'\]|\[|\.|\)|\(',  # Clear unnecessary stuff
							   '',
							   country_coordinates[key].upper())
									if key in country_coordinates else 'N/A',
					fill_color=color_creator(item),
					color='red',
					fill_opacity=0.4,
					tooltip='Press here'))
		except ValueError:
			continue

	fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
											 encoding='utf-8-sig').read(),
								   style_function=lambda x:
								   {
									   'fillColor': 'green'
									   if x['properties']['AREA'] < 100000
									   else 'orange'
								   }))

	folium.TileLayer('Stamen Toner',
					 attr='XXX Mapbox Attribution').add_to(map_data)
	folium.TileLayer('Mapbox Control Room',
					 attr='XXX Mapbox Attribution').add_to(map_data)
	map_data.add_child(fg_all_movies)
	map_data.add_child(fg_year_movie)
	map_data.add_child(fg_pp)
	map_data.add_child(folium.LayerControl())
	pathlib.Path('maps').mkdir(exist_ok=True)  # Create empty <maps> dir
	map_data.save('maps/Map{}.html'.format(str(user_year)))
	print('Map saved successfully!')


def main(create_csv=True):
	"""
    Launches the program and all necessary functions.

    None -> None

    Usage:
    > main()
    """
	print('Greetings!')
	choices = choose_file_location()  # List of filenames
	if create_csv:
		get_places_from_file(choices[0], choices[1])
		find_coordinates(choices[1], choices[2], choices[3])
	year = read_user_input()  # Year of movies to search
	build_map(choices[2], choices[3], year)  # Main map building function
	print('The program has finished successfully!')


if __name__ == '__main__':
	main(create_csv=False)  # 3.. 2.. 1.. Launch!
