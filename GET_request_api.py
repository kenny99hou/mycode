import requests

# The API endpoint (URL)
url = "https://jsonplaceholder.typicode.com/todos/1"

try:
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (Status Code 200)
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        print("Success!")
        print(f"Title: {data['title']}")
        print(f"Full Data: {data}")
    else:
        print(f"Request failed with status: {response.status_code}")

except requests.exceptions.RequestException as e:
    # Handle connection errors (e.g., no internet, server down)
    print(f"An error occurred: {e}")
