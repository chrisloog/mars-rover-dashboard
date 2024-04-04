
# Mars Rover Picture Dashboard

The Mars Rover Dashboard is a Python program that allows users to interactively explore photos captured by various Mars rovers. Users can select a specific rover, choose a camera, and enter a date to retrieve a photo taken by the selected rover on the specified date using the NASA API.

### Features

1. Choose a specific rover (Curiosity, Spirit, Opportunity) or select a random one.
2. Select a camera from the available options for the chosen rover.
3. Enter a date within the mission duration of the rover or select a random date.
4. View information about the selected rover, including its landing date, launch date, mission status, maximum date with available photos, and total number of photos.
5. Download and save the selected photo to a local directory.
6. Retry the selection process or exit the program.

### How to Use

1. Clone the repository to your local machine.
2. Set up your NASA API key as an environment variable named NASA_API_KEY.
3. Run the program by executing the menu_system.py script.
4. Follow the prompts to select a rover, camera, and date, and retrieve photos from Mars.

### Dependencies

Python 3.x
requests library
NASA API key (obtainable from the NASA API website)
