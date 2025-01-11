import asyncio
import aiohttp  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import logging

# Configure logging
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] | %(message)s",
    level=logging.DEBUG,  # You can change this to INFO, WARNING, ERROR, etc.
)

BASE_URL = "https://www.root-me.org"
ROOT_ME_USERS = [
    "Drachh",
    "Kalith",
    "Hioav2",
    "ManJiRaw",
    "Mac-812606",
    "draune",
    "Snaxx",
    "AyWiZz",
    "Xeroxx75",
    "Onyx-852889",
    "Chelinka",
]


MAX_RETRIES = 3  # Maximum number of retries for connection-related issues
RETRY_DELAY = 5  # Delay between retries in seconds


# Define a function to fetch user data with retries
async def get_user_data(username):
    url = f"{BASE_URL}/{username}"
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            # Use aiohttp to make the request asynchronously
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=20
                ) as response:  # Timeout set to 20 seconds
                    response.raise_for_status()  # Raise an exception for HTTP errors

                    # Handle rate-limiting (HTTP 429)
                    if response.status == 429:
                        retry_after = response.headers.get("Retry-After")
                        retry_delay = int(retry_after) if retry_after else RETRY_DELAY
                        logging.debug(
                            f"Rate-limited. Retrying after {retry_delay} seconds..."
                        )
                        await asyncio.sleep(retry_delay)
                        continue  # Retry the request

                    return (
                        await response.text()
                    )  # Await the response text asynchronously

        except asyncio.TimeoutError:
            logging.debug(
                f"Request timed out while fetching data for {username}. Attempt {attempt + 1}/{MAX_RETRIES}"
            )
            break  # Stop retrying if timeout occurs

        except aiohttp.ClientError as e:
            logging.error(
                f"Error fetching data for {username}: {e}. Attempt {attempt + 1}/{MAX_RETRIES}"
            )
            attempt += 1
            if attempt >= MAX_RETRIES:
                logging.error(f"Max retries reached for {username}.")
                break
            await asyncio.sleep(RETRY_DELAY)  # Wait before retrying

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

        # logging.info the results for the current user
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
        logging.info(f"Failed to fetch or parse data for {username}.")
        return None


# Define an async function to fetch and parse user data for all users
async def fetch_and_parse_users():
    all_stats = []
    for username in ROOT_ME_USERS:
        data = await get_user_data(username)
        if data is None:
            continue
        else:
            user_stats = parse_user_data(username, data)
            all_stats.append(user_stats)
        await asyncio.sleep(5)  # Add a delay between requests to avoid rate limiting
    return all_stats
