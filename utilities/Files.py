import json
import os
import requests
from pathlib import Path


def writeFile(fileName, Data):
    with open(fileName, "w", encoding='utf-8') as file:
        file.write(Data)
    file.close()


def readJsonFile(fileName):
    try:
        with open(fileName, "rb") as file:
            return json.load(file)
    except IOError as err:
        if err.errno == 2:  # File didn't exist, no biggie
            return {}
        else:  # Something weird, just re-raise the error
            raise


def ensureDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def readFile(fileName):
    with open(fileName, "r") as file:
        data = file.read()
        file.close()
    return data



# Function to extract data from the API
def extract_data_from_api(url, headers=None):
    try:
        # Send a GET request to the API
        response = requests.get(url, headers=headers)

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.text
            return data
        else:
            # Handle non-successful response
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        print(f"An error occurred: {e}")
        return None

def header(string):
    x = len(string)*"="
    print(f"{string}\n{x}\n")


def get_paths(root, home, file_name, repo_tail):
    home_path = Path(home)
    bi_path = home_path / f'{root}/'
    bi_auth = home_path / 'auth/'
    data_path = home_path / f'temp/data/{root}/{repo_tail}'
    logs_path = home_path / f'temp/logs/{root}/{repo_tail}'
    folder_name = Path(os.path.dirname(file_name))
    return bi_path, bi_auth, data_path, logs_path, folder_name