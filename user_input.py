"""This is the file that takes in user input via the drop-down menys on our UI, and saves the
user data in variables for us to make predictions on. We are using the library tkinter for the UI."""

import tkinter as tk
from typing import Any


def display_user_input() -> tuple:
    """Display interactive UI"""
    root = tk.Tk()
    root.title("Culinary Connections")
    root.geometry('1000x600')

    def save_results() -> tuple:
        """Save the user's choices into variables."""

        user_input_final = []

        user_area = area_nashville.get()
        input_cuisine = cuisine_type.get()
        input_takeout = takeout_type.get()
        input_star_rating = star_rating_type.get()
        input_alcohol = alcohol_type.get()
        input_wifi = wifi_type.get()
        input_credit_card = credit_card_type.get()
        input_group = group_type.get()
        input_price = price_type.get()

        user_input_final.append(input_cuisine)

        if input_takeout == 'Takeout':
            user_input_final.append('takeout')
        else:
            user_input_final.append('no takeout')

        if input_star_rating == '3+ stars':
            user_input_final.append('high star')
        else:
            user_input_final.append('low star')

        if input_alcohol == 'Alcohol':
            user_input_final.append('alcohol')
        else:
            user_input_final.append('no alcohol')

        if input_wifi == 'Wi-Fi Available':
            user_input_final.append('wifi')
        else:
            user_input_final.append('no wifi')

        if input_credit_card == 'Credit Card':
            user_input_final.append('credit card')
        else:
            user_input_final.append('no credit card')

        if input_group == 'Dining with a Group':
            user_input_final.append('groups')
        else:
            user_input_final.append('no groups')

        user_input_final.append(input_price)
        return user_area, user_input_final

    def return_save_results(_event: Any) -> tuple:
        """Allows us to access the returned value of save_results while we're doing UI stuff."""
        result = save_results()
        return result

    # The background image
    bgimg = tk.PhotoImage(file="food_background.png")
    limg = tk.Label(root, image=bgimg)
    limg.pack()

    main_frame = tk.LabelFrame(
        root,
        text='Enter your preferences here!',
    )

    main_frame.place(anchor='center', relx=0.5, rely=0.21)

    # INITIALIZING VARIABLES
    area_nashville = tk.StringVar()
    cuisine_type = tk.StringVar()
    takeout_type = tk.StringVar()
    star_rating_type = tk.StringVar()
    alcohol_type = tk.StringVar()
    wifi_type = tk.StringVar()
    credit_card_type = tk.StringVar()
    group_type = tk.StringVar()
    price_type = tk.StringVar()

    # LABLES
    area_nashville_label = tk.Label(main_frame, text="Which area of Nashville are you located in?")
    area_nashville_label.grid(row=1, column=0)

    cuisine_label = tk.Label(main_frame, text="What type of cuisine do you prefer?")
    cuisine_label.grid(row=2, column=0)

    takeout_label = tk.Label(main_frame, text="Do you want takeout?")
    takeout_label.grid(row=3, column=0)

    star_rating_label = tk.Label(main_frame, text="How should the restaurant be rated?")
    star_rating_label.grid(row=4, column=0)

    alcohol_label = tk.Label(main_frame, text="Do you prefer the restaurant serves alcohol?")
    alcohol_label.grid(row=5, column=0)

    wifi_label = tk.Label(main_frame, text="Do you want Wi-Fi at the restaurant?")
    wifi_label.grid(row=6, column=0)

    credit_card_label = tk.Label(main_frame, text="How would you like to pay?")
    credit_card_label.grid(row=7, column=0)

    group_label = tk.Label(main_frame, text="Who are you dining with?")
    group_label.grid(row=8, column=0)

    price_label = tk.Label(main_frame, text="What price range do you prefer?")
    price_label.grid(row=9, column=0)

    # OPTIONS
    area_nashville_options = ['Downtown', 'East Nashville', 'The Gulch', 'Germantown', '12 South',
                              'Green Hills', 'Belmont-Hillsboro', 'Joelton']
    cuisine_options = ['American', 'Chinese', 'Greek', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Tex-Mex',
                       'Vegetarian', 'Asian', 'Mediterranean', 'Seafood', 'Southern']
    takeout_options = ['Takeout', 'Dine In']
    star_rating_options = ['3+ stars', '3- stars (Who cares about the rating anyway?)']
    alcohol_options = ['Alcohol', 'No Alcohol']
    wifi_options = ['Wi-Fi Available', 'Wi-Fi not needed!']
    credit_card_options = ['Credit Card', 'Cash Only']
    group_options = ['Dining with a Group', 'No Group!']
    price_options = ['$', '$$', '$$$', '$$$$']

    # DROP-DOWN MENUS
    area_nashville_menu = tk.OptionMenu(main_frame, area_nashville, *area_nashville_options)
    area_nashville_menu.grid(row=1, column=1)

    cuisine_menu = tk.OptionMenu(main_frame, cuisine_type, *cuisine_options)
    cuisine_menu.grid(row=2, column=1)

    takeout_menu = tk.OptionMenu(main_frame, takeout_type, *takeout_options)
    takeout_menu.grid(row=3, column=1)

    star_rating_menu = tk.OptionMenu(main_frame, star_rating_type, *star_rating_options)
    star_rating_menu.grid(row=4, column=1)

    alcohol_menu = tk.OptionMenu(main_frame, alcohol_type, *alcohol_options)
    alcohol_menu.grid(row=5, column=1)

    wifi_menu = tk.OptionMenu(main_frame, wifi_type, *wifi_options)
    wifi_menu.grid(row=6, column=1)

    credit_card_menu = tk.OptionMenu(main_frame, credit_card_type, *credit_card_options)
    credit_card_menu.grid(row=7, column=1)

    group_menu = tk.OptionMenu(main_frame, group_type, *group_options)
    group_menu.grid(row=8, column=1)

    price_menu = tk.OptionMenu(main_frame, price_type, *price_options)
    price_menu.grid(row=9, column=1)

    # SAVE RESULTS (BUTTON)
    save_button = tk.Button(root, text="Save Results")
    save_button.place(anchor='center', relx=0.5, rely=0.48)
    save_button.bind("<Button-1>", return_save_results)

    # TEXT INSTRUCTIONS
    instruction_text = tk.Label(root, text='After clicking Save Results, close this window!!!!!!!')
    instruction_text.place(anchor='s', relx=0.5, rely=0.6)

    guide_text = tk.Label(root, text='MAP GUIDE: Yellow markers = YOUR Personalized Recommendations')
    guide_text.place(anchor='s', relx=0.5, rely=0.7)

    more_text = tk.Label(root, text='Blue markers = General Restaurants in Your Area')
    more_text.place(anchor='s', relx=0.5, rely=0.8)

    root.mainloop()

    # Return (user_area, user_input_final)
    return return_save_results(None)


def display_makefriends() -> tuple:
    """Open window for user to make friend."""
    root2 = tk.Tk()
    root2.title("Culinary Connections")
    root2.geometry('1000x600')

    def make_friend() -> tuple:
        """Save the friend's name."""
        input_friend = friend.get()
        input_name = user_name.get()
        return input_name, input_friend

    def return_make_friend(_event: Any) -> tuple:
        """Allows us to access the returned value of make_friend while we're doing UI stuff."""
        result = make_friend()
        return result

    bgimg = tk.PhotoImage(file="food_background.png")
    limg = tk.Label(root2, image=bgimg)
    limg.pack()

    friend_frame = tk.LabelFrame(
        root2,
        text='Make a friend here!'
    )

    friend_frame.place(anchor='s', relx=0.5, rely=0.5)

    friend = tk.StringVar()
    user_name = tk.StringVar()

    name_label = tk.Label(friend_frame, text='Enter your name: ')
    name_label.grid(row=1, column=1)

    friend_label = tk.Label(friend_frame, text='Enter the name of the friend you want to make: ')
    friend_label.grid(row=2, column=1)

    name_menu = tk.Entry(friend_frame, textvariable=user_name)
    name_menu.grid(row=1, column=2)

    friend_menu = tk.Entry(friend_frame, textvariable=friend)
    friend_menu.grid(row=2, column=2)

    # MAKE FRIEND (BUTTON)
    friend_button = tk.Button(root2, text="Make Friend")
    friend_button.place(anchor='center', relx=0.5, rely=0.9)
    friend_button.bind("<Button-1>", return_make_friend)

    make_friends_text = tk.Label(root2, text='After filling this out, close this window!!!!!')
    make_friends_text.place(anchor='s', relx=0.5, rely=0.3)

    guide_text = tk.Label(root2, text='MAP GUIDE: Yellow markers = YOUR Personalized Recommendations')
    guide_text.place(anchor='s', relx=0.5, rely=0.6)

    more_text = tk.Label(root2, text='Blue markers = General Restaurants in Your Area')
    more_text.place(anchor='s', relx=0.5, rely=0.7)

    red_text = tk.Label(root2, text='Red markers = Restaurants Recommended by Your Friend')
    red_text.place(anchor='s', relx=0.5, rely=0.8)

    root2.mainloop()

    # (your_name, friend_name)
    return return_make_friend(None)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 300,
        'disable': ['E1136', 'W0221', 'R0914', 'R0915'],
        'max-nested-blocks': 4,
        'extra-imports': ['tkinter']
    })
