"""The main file to run!"""

import graph_implement
import tree_implement
import folium
import name_implement
import user_input

all_user_data = user_input.display_user_input()

# all_r_data reads data and stores it as a list
all_r_data = tree_implement.unzip_data('yelp_academic_dataset_business.json.zip', 'yelp_academic_dataset_business.json')

# filter data to only include restaurants in Nashville
r_data = tree_implement.filter_businesses_nashville(all_r_data)

# create a list of all cuisines present in the restaurant data
list_of_cuisines = tree_implement.filter_cuisine(r_data, 'cuisines.txt')

# create the decision tree
decision_tree = tree_implement.make_tree(r_data, list_of_cuisines)

# generating a list of restaurants based on the user's specifications
recommended_restaurants = decision_tree.match_user_restaurant(all_user_data[1])

# generate a dummy data for the users who have used the program
user_data = name_implement.generate_users(30, 5)

# create a map on folium centered at Nashville
map = folium.Map(location=[36.1627, -86.7816], zoom_start=12)

# get the latitude and longitude of the location entered by the user
# here, location is the location that the user chose
user_location = graph_implement.get_lat_lon(all_user_data[0])

# create a graph
g = graph_implement.Graph()

# add the vertices and edges based on the dummy data (user_data)
g.load_restaurant_graph(r_data, user_data)

# get the restaurants that are close to the user
nearby_r_data = g.get_nearby_restaurants(user_location, r_data, user_data)

# get the data for the all the restaurants in recommended_restaurants
rr_data = tree_implement.recommended_to_dict(recommended_restaurants, r_data)

# show restaurants from the decision tree
g.show_restaurants_connected(map, rr_data, 'decision_tree')

# show restaurants closeby to the user in folium
g.show_restaurants_connected(map, nearby_r_data, 'nearby')

friending_data = user_input.display_makefriends()

# get user's and friend's names
user = friending_data[0]
friend = friending_data[1]

# adding the user to the graph network
g.user_to_restaurant(user, recommended_restaurants)

# create an edge between the user and friend so that they become neighbours
g.make_friend(user, friend)

# get data for all the restaurants that the friend is adjacent to
f_restaurants = g.get_friend_restaurants(friend, r_data)

# show the restaurants from the decision tree, nearby to the user, and recommended by friend if there are overalaps
# between friend and the other two categories, then the marker will be shown as recommended by friend
g.show_restaurants_connected(map, f_restaurants, 'friend')






