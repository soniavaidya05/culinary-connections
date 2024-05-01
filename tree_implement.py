"""Tree time!"""
from __future__ import annotations
import zipfile
import json
from typing import Any, Optional
import os

from python_ta.contracts import check_contracts


@check_contracts
class Tree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def insert_sequence(self, items: list) -> None:
        """Insert the given items into this tree, forming a chain of descnedants. Pathways with sequences in common will
        follow the same path until they eventually diverge.

        """
        if not items:
            return

        else:
            item = items[0]
            new_tree = Tree(item, [])

            curr_subtree = new_tree

            for sub in self._subtrees:
                if sub._root == item:
                    curr_subtree = sub

            if curr_subtree == new_tree:
                self._subtrees.append(new_tree)

            curr_subtree.insert_sequence(items[1:])

    def match_user_restaurant(self, user_input: list) -> list:
        """This function traverses restaurant data tree to determine the possible restaurant(s) that match the
        user input, and print the result.
        """

        if len(user_input) <= 0 and not self._subtrees:
            return []

        elif len(user_input) <= 0:
            possible_restaurants = []

            accum = 0
            for r_tree in self._subtrees:
                accum += 1
                if accum <= 10:
                    possible_restaurants.append(r_tree._root)
                else:
                    break

            return possible_restaurants

        else:
            curr_subtree = self._subtrees
            restaurant_attribute = user_input[0]
            for sub in self._subtrees:
                if sub._root == restaurant_attribute:
                    curr_subtree = sub
                    break
            if curr_subtree == self._subtrees:
                return []
            else:
                return curr_subtree.match_user_restaurant(user_input[1:])


def unzip_data(zip_path: str, json_file_name: str) -> list:
    """Get json data (all business data from yelp)."""

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(json_file_name)

    with open(json_file_name, 'r') as f:
        all_data = [json.loads(line) for line in f]

    return all_data


# filtering the business dataset to get that of only restaurants in Nashville
def filter_businesses_nashville(all_data: list) -> list:
    """Filter the dataset to only include restaurants in Nashville."""
    restaurant_data = []
    for d in all_data:
        if d.get('categories') is not None:
            if ('Food' in d['categories'] or 'Restaurant' in d['categories']) and d['city'] == 'Nashville':
                restaurant_data.append(d)

    assert all(de['city'] == 'Nashville' for de in restaurant_data)
    return restaurant_data


# creating a list of cuisines available in the dataset
def filter_cuisine(r_data: list, cuisine_file: str) -> list:
    """Return a list of all cuisines present in the r_data based on the cuisines present in cuisine_file."""
    food_list = []
    for dictionary in r_data:
        food_list.extend(dictionary['categories'].split())
    food_count = {}
    for food in food_list:
        if food not in food_count:
            food_count[food] = food_list.count(food)
    with open(cuisine_file, "r") as f:
        cuisine = []
        for line in f:
            cuisine.append(line.strip())
    cuisine_list = []
    for c in cuisine:
        if c in food_count and food_count[c] > 12:
            cuisine_list.append(c)
    return cuisine_list


def make_tree(restaurant_data: list, cuisine_list: list) -> Tree:
    """Make a tree from the restaurant data attributes we chose to make available to the user from dataset."""
    central_tree = Tree('', [])
    # r_rows = []
    for r in restaurant_data:
        if isinstance(r, dict):
            row = []

            # What kind of food are you craving? (FOOD CATEGORY)
            # After running the function list_of_cuisines we get the list of potential cuisines
            # (PARAMETER OF THIS FUNCTION)
            try:
                cuisine_contains = False
                for cuisine in cuisine_list:
                    if cuisine in r['categories']:
                        row.append(cuisine)
                        cuisine_contains = True
                        break
                if cuisine_contains is False:
                    continue
            except KeyError:
                continue

            # TakeOut option (YES/NO)
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']['RestaurantsTakeOut'] == 'True':
                        row.append('takeout')
                    elif r['attributes']['RestaurantsTakeOut'] == 'False':
                        row.append('no takeout')
                    else:
                        continue

            except KeyError:
                continue

            # Do you have a preference for star rating? (RATING) YES/NO
            try:
                if r['stars'] >= 3.0:
                    row.append('high star')
                elif r['stars'] < 3.0:
                    row.append('low star')
                else:
                    continue
            except KeyError:
                continue

            # Would you prefer the option to drink alcohol at the restaurant? (ALCOHOL) YES/NO
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']['Alcohol'] == "u'none'":
                        row.append('no alcohol')
                    elif r['attributes']['Alcohol'] != "u'none'":
                        row.append('alcohol')
                    else:
                        continue
            except KeyError:
                continue

            # Would you prefer having WiFi at the restaurant? (WIFI) YES/NO
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']['WiFi'] == "'no'":
                        row.append('no wifi')
                    elif r['attributes']['WiFi'] != "'no'":
                        row.append('wifi')
                    else:
                        continue
            except KeyError:
                continue

            # Do you need to pay with credit card? (CREDIT CARD) YES/NO
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']["BusinessAcceptsCreditCards"] == 'True':
                        row.append('credit card')
                    elif r['attributes']["BusinessAcceptsCreditCards"] != 'True':
                        row.append('no credit card')
                    else:
                        continue
            except KeyError:
                continue

            # Are you eating with a group? (YES/NO)
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']['RestaurantsGoodForGroups'] == 'True':
                        row.append('groups')
                    elif r['attributes']['RestaurantsGoodForGroups'] != 'True':
                        row.append('no groups')
                    else:
                        continue
            except KeyError:
                continue

            # On a scale of 1 to 4 what kind of pricing do you prefer? ($, $$, $$$, $$$$)
            try:
                if isinstance(r['attributes'], dict):
                    if r['attributes']['RestaurantsPriceRange2'] == '1':
                        row.append('$')
                    elif r['attributes']['RestaurantsPriceRange2'] == '2':
                        row.append('$$')
                    elif r['attributes']['RestaurantsPriceRange2'] == '3':
                        row.append('$$$')
                    elif r['attributes']['RestaurantsPriceRange2'] == '4':
                        row.append('$$$$')
                    else:
                        continue
            except KeyError:
                continue

            # Adding the restaurant name as a leaf
            try:
                row.append(r['name'])
            except KeyError:
                continue

            # r_rows.append(row)
            central_tree.insert_sequence(row)

    return central_tree


def recommended_to_dict(r_restaurants: list, r_data: list[dict]) -> list[dict]:
    """Return the corresponding dictionaries to recommended_restaurants."""
    r_d = []
    for business in r_data:
        for restaurant in r_restaurants:
            if business['name'] == restaurant:
                r_d.append(business)
    return r_d


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 300,
        'disable': ['E1136', 'W0221', 'R0915', 'R0912', 'R1702'],
        'max-nested-blocks': 4,
        'extra-imports': ["json", "zipfile", "os"],
        'allowed-io': ['unzip_data', 'filter_cuisine']
    })
