import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.root-me.org"
USERNAME = "snaxx"

def get_user_info(username):
    url = f"{BASE_URL}/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(response)
        print(f"Failed to get user info for {username}")

data = get_user_info(USERNAME)

# Parse the HTML content
soup = BeautifulSoup(data, 'html.parser')

divs = soup.find_all("div", class_="small-6 medium-3 columns text-center")

# Extract labels and values
results = {}
for div in divs:
    # Extract the value (text after &nbsp;)
    value = div.find("h3").get_text(strip=True).split("\u00a0")[-1]
    
    # Extract the label (text inside <span class="gras">)
    label = div.find("span", class_="gras").get_text(strip=True)
    
    # Store the result
    results[label] = value


# Print the results
for label, value in results.items():
    print(f"{label}: {value}")

