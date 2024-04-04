import mars_rover_api as rover
import random as rnd
import datetime


def run():
    while True:
        rover_choice = (input(
            "Would you like to get a picture from a specific rover (Curiosity, Spirit, Opportunity) or random? ")
                        .lower()
                        .strip())

        if is_random(rover_choice):
            rover_name = rnd.choice(list(rover.info.keys()))
            print(f"\nYou landed on rover {rover_name.capitalize()}!")
        elif rover_choice in rover.info:
            rover_name = rover_choice
            print(f"\nYou chose rover {rover_name.capitalize()}!")
        else:
            print("Please enter a valid rover name or choose a random one.")
            continue

        print("Available cameras for your rover are", ", ".join(rover.info[rover_name]["cameras"]))

        while True:
            camera_choice = input(
                f"\nWould you like a picture from a specific camera or a random one? ").upper().strip()
            if is_random(camera_choice.lower()):
                rover_camera = rnd.choice(list(rover.info[rover_name]["cameras"]))
                break
            elif camera_choice in rover.info[rover_name]["cameras"]:
                rover_camera = camera_choice
                break
            else:
                print("Please enter a valid rover camera or choose a random one")

        manifest = rover.get_manifest(rover_name)

        while True:
            earth_date_input = input(
                f"\nEnter a date (between {manifest['landing_date']} and {manifest['max_date']}) "
                f"or press enter for a random date: "
            )
            if not earth_date_input:
                earth_date = rnd.choice([date['earth_date'] for date in manifest['photos']])
                break
            try:
                earth_date = datetime.datetime.strptime(earth_date_input, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                continue

            if earth_date < datetime.datetime.strptime(manifest['landing_date'], '%Y-%m-%d').date() \
                    or earth_date > datetime.datetime.strptime(manifest['max_date'], '%Y-%m-%d').date():
                print("Invalid date. Please enter a date within the range.")
            else:
                break

        photo_url = rover.fetch_photo(rover_name, earth_date, rover_camera)

        MAX_ATTEMPTS = 5

        attempts = 0

        while not photo_url:
            attempts += 1
            print("Selecting the closest date.")
            dates = [date['earth_date'] for date in manifest['photos']]
            closest_date = min(dates, key=lambda x: abs(
                datetime.datetime.strptime(x, '%Y-%m-%d').date() - datetime.datetime.strptime(str(earth_date),
                                                                                              '%Y-%m-%d').date()))
            photo_url = rover.fetch_photo(rover_name, closest_date, rover_camera)
            earth_date = closest_date

            if attempts >= MAX_ATTEMPTS:
                print(f"Reached maximum attempts ({MAX_ATTEMPTS}). No photos found.")
                break

        rover.save_photo(rover_name, rover_camera, str(earth_date), photo_url)

        another_try = input("\nDo you want to try again? (y/n): ")
        if another_try.lower() != "y":
            break


def is_random(user_selection):
    return user_selection == "r" or user_selection == "random"
