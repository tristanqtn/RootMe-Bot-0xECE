import asyncio
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.root-me.org"
users = ["Mac-812606", "Drachh", "Snaxx", "NathanTmor"]


# Define a function to fetch user information with better error handling and timeout
async def get_user_data(username):
    url = f"{BASE_URL}/{username}"
    try:
        # Use aiohttp to make the request asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, timeout=20
            ) as response:  # Timeout set to 10 seconds
                response.raise_for_status()  # Raise an exception for HTTP errors
                return await response.text()  # Await the response text asynchronously
    except asyncio.TimeoutError:
        print(f"Request timed out while fetching data for {username}")
        return None
    except aiohttp.ClientError as e:
        print(f"Error fetching data for {username}: {e}")
        return None


# Parse the user data (extracting relevant details)
def parse_user_data(username, data):
    stats = {}
    stats["Username"] = username
    if data:
        # Parse the HTML content
        soup = BeautifulSoup(data, "html.parser")

        # Find all the relevant divs
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

        # Print the results for the current user
        for label, value in results.items():
            stats[label] = value

        # Extract the last challenge
        chall = soup.find("img", src="squelettes/img/activitees.svg?1570951387")
        if chall:
            chall = chall.find_next("a")
            last_challenge = chall.get_text(strip=True)
            stats["Last Challenge"] = last_challenge
            return stats
    else:
        print(f"Failed to fetch or parse data for {username}.")
        return None


# Define an async function to fetch and parse user data for all users
async def fetch_and_parse_users():
    all_stats = []
    for username in users:
        data = await get_user_data(username)
        if data is None:
            continue
        else:
            user_stats = parse_user_data(username, data)
            all_stats.append(user_stats)
        await asyncio.sleep(5)  # Add a delay between requests to avoid rate limiting
    return all_stats
