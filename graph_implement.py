"""Graph time!"""
from __future__ import annotations
from typing import Any
import subprocess
import folium
from geopy.distance import geodesic


class _Vertex:
    """A vertex in a restaurant review graph, used to represent a user or a restaurant.

    Each vertex item is either a user or restaurant title. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent with lecture.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or restaurant.
        - kind: The type of this vertex: 'user' or 'restaurant'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'restaurant'}
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'restaurant'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()


class Graph:
    """A graph used to represent a restaurant review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def user_to_restaurant(self, user: str, restaurants: list) -> None:
        """Takes restaurants given by the decision tree, adds the user to the graph, and creates edges between the
        user and the recommended restaurants"""
        self.add_vertex(user, 'user')
        for r in restaurants:
            self.add_vertex(r, 'restaurant')
            self.add_edge(user, r)

    def show_restaurants_connected(self, my_map: folium.Map, r_data: list[dict], category: str) -> None:
        """Displays each restaurant and its user neighbours on folium."""

        for v in self._vertices:
            for business in r_data:
                vertex = self._vertices[v]
                if 'restaurant' == vertex.kind and business['name'] == vertex.item:
                    people_list = list(self.get_neighbours(vertex.item))
                    people_str = ", ".join(people_list)
                    popup_html = (f"<div style='font-family: trebuchet ms, sans-serif; font-size: "
                                  f"15px;'><b>Restaurant:</b> {business['name']}<br/>")
                    popup_html += f"<div style='margin-top: 9px;'><b>Rating:</b> {business['stars']}<br/>"
                    popup_html += f"<div style='margin-top: 9px;'><b>People:</b> {people_str}<br/>"
                    popup_iframe = folium.IFrame(width=220, height=110, html=popup_html)
                    b_location = [business['latitude'], business['longitude']]
                    make_marker(category, b_location, popup_iframe, my_map)

        my_map.save("map.html")
        subprocess.run(["open", 'map.html'], check=True)

    def load_restaurant_graph(self, r_data: list[dict], user_data: list[dict]) -> None:
        """Create an edges between users and corresponding restaurants based on r_data and user_data."""
        for business in r_data:
            user_list = give_user(user_data)
            for user in user_list:
                if business['name'] in user[1]:
                    self.add_to_graph((user[0], 'user'), (business['name'], 'restaurant'))

    # the r_data in this method is the entire data of restaurants in Nashville
    def get_nearby_restaurants(self, user_location: tuple, r_data: list[dict], user_data: list[dict]) -> list[dict]:
        """Returns the eateries within 1 km of their location."""
        self.load_restaurant_graph(r_data, user_data)
        nearby_so_far = []
        for business in r_data:
            user_list = give_user(user_data)
            for user in user_list:
                b_location = (business['latitude'], business['longitude'])
                if distance(user_location, b_location) and business['name'] in user[1]:
                    self.add_to_graph((user[0], 'user'), (business['name'], 'restaurant'))
                    nearby_so_far.append(business)
        if len(nearby_so_far) > 5:
            return nearby_so_far[:5]
        return nearby_so_far

    def add_to_graph(self, u: tuple, r: tuple) -> None:
        """Create user and restaurant vertices and add edges between them."""
        self.add_vertex(u[0], u[1])
        self.add_vertex(r[0], r[1])
        self.add_edge(u[0], r[0])

    def make_friend(self, user: str, friend: str) -> None:
        """Create an edge between user and friend."""
        self.add_edge(user, friend)

    def get_friend_restaurants(self, friend: str, r_data: list[dict]) -> list[dict]:
        """Return information on all restaurants friend is connected to."""
        restaurants_so_far = []
        all_neigh = list(self.get_neighbours(friend))
        r_neigh = [neigh for neigh in all_neigh if self._vertices[neigh].kind == 'restaurant']
        for business in r_data:
            for restaurant in r_neigh:
                if business['name'] == restaurant:
                    restaurants_so_far.append(business)
        return restaurants_so_far


def distance(user_location: tuple, b_location: tuple) -> bool:
    """Returns whether the distance between user_location and b_location is less than 1km."""
    distance_between = geodesic(user_location, b_location).kilometers
    return distance_between <= 1


def make_marker(category: str, b_location: list, popup_iframe: folium.IFrame, my_map: folium.Map) -> None:
    """Make a marker on the folium map based on type, color, and b_location."""
    if category == 'friend':
        color = 'red'
    elif category == 'decision_tree':
        color = 'orange'
    else:
        color = 'blue'

    folium.Marker(b_location, popup=folium.Popup(popup_iframe),
                  icon=folium.Icon(color=color, icon='glyphicon glyphicon-cutlery')).add_to(my_map)


def give_user(user_data: list[dict]) -> list[tuple[str, list]]:
    """Return user_data in a list with tuples."""
    lst_so_far = []
    for user in user_data:
        for user_name in user:
            lst_so_far.append((user_name, user[user_name]))
    return lst_so_far


def get_lat_lon(location: str) -> tuple[float, float]:
    """Return the latitude and longitude based on the location."""
    locations = {
        "Downtown": (36.1627, -86.7816),
        "East Nashville": (36.1771, -86.7538),
        "The Gulch": (36.1525, -86.7889),
        "Germantown": (36.1771, -86.7907),
        "12 South": (36.1230, -86.7909),
        "Green Hills": (36.1069, -86.8190),
        "Belmont-Hillsboro": (36.1314, -86.7996),
        "Joelton": (36.3239, -86.8689)
    }
    return locations[location]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 237,
        'extra-imports': ["geopy.distance", "folium", "subprocess"]
    })
