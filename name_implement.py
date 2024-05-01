"""...
"""
import csv
import io
import random
from python_ta.contracts import check_contracts
import tree_implement


def read_names_from_csv(filename: str) -> list:
    """
    Reads names from a CSV file and returns them as a list.

    Args:
        filename (str): The name of the CSV file to read.

    Returns:
        list: A list containing the names extracted from the CSV file.
    """
    names = []
    with io.open(filename, 'r') as file_name:
        csv_reader = csv.reader(file_name)
        for rows in csv_reader:
            names.append(rows[0])
    return names


@check_contracts
def generate_dummy_data(num_records: int) -> list:
    """
    Generate dummy data

    >>> generate_dummy_data(3)
    [{'name': 'Julie'}, {'name': 'Amanda'}, {'name': 'Ruffus'}]
    """
    names = read_names_from_csv('names.csv')
    dummy_data = []
    for _ in range(num_records):
        name = random.choice(names)
        dummy_data.append({"name": name})
    return dummy_data


@check_contracts
def restaurant_finder(cuisine: str) -> list:
    """
     Find restaurants that serve the specified cuisine.

    Parameters:
        cuisine (str): The cuisine to search for.

    Returns:
        list: A list of names of restaurants serving the specified cuisine.
    """
    yelp_zip = 'yelp_academic_dataset_business.json.zip'
    yelp_json = 'yelp_academic_dataset_business.json'
    all_r_data = tree_implement.unzip_data(yelp_zip, yelp_json)
    r_data = tree_implement.filter_businesses_nashville(all_r_data)
    r_w_c = [yelp["name"] for yelp in r_data if cuisine in yelp["categories"]]

    return r_w_c


@check_contracts
def generate_users(user_amount: int, max_restaurants_per_user: int) -> list:
    """
    Generate dummy users with limited restaurants.
    """
    cuisine1 = ['Mexican', 'Southern', 'American', 'Italian', 'Seafood']
    cuisine2 = ['Mediterranean', 'Asian', 'Japanese', 'Tex-Mex', 'Fusion']
    cuisine3 = ['Vegetarian', 'Vegan', 'Ethnic', 'Greek', 'Thai', 'Gluten-Free']
    cuisine4 = ['Caribbean', 'French', 'Indian', 'Chinese', 'Vietnamese']
    cuisine = cuisine1 + cuisine2 + cuisine3 + cuisine4
    users = generate_dummy_data(user_amount)

    final_users = []
    for user in users:
        cui = random.choice(cuisine)

        restaurants = restaurant_finder(cui)[:max_restaurants_per_user]
        final_users.append({user["name"]: restaurants})

    return final_users

# example use
# users_for_use = generate_dummy_users(10, 5)
# print(users_for_use)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["csv", "io", "random", "tree_implement"]
    })
