import requests

url = "https://jsonplaceholder.typicode.com/posts"

# Data to send (payload)
payload = {
    "title": "My New Post",
    "body": "This is the content of my post.",
    "userId": 1
}

# Headers (often used for authentication keys)
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    # "Authorization": "Bearer YOUR_API_TOKEN"  <-- If the API requires a token
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:  # 201 usually means 'Created'
    print("Resource created successfully!")
    print(response.json())
else:
    print(f"Failed: {response.status_code}")
