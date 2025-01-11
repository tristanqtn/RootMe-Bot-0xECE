import asyncio
import aiohttp  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import logging
import sqlite3

# Configure logging
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] | %(message)s",
    level=logging.DEBUG,  # You can change this to INFO, WARNING, ERROR, etc.
)

DATABASE_PATH = "users.db"  # Path to the SQLite database
BASE_URL = "https://www.root-me.org"
MAX_RETRIES = 3  # Maximum number of retries for connection-related issues
RETRY_DELAY = 5  # Delay between retries in seconds


# Function to fetch user data with retries
async def get_user_data(username):
    url = f"{BASE_URL}/{username}"
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=20
                ) as response:  # Timeout set to 20 seconds
                    response.raise_for_status()  # Raise an exception for HTTP errors

                    if response.status == 429:  # Handle rate-limiting (HTTP 429)
                        retry_after = response.headers.get("Retry-After")
                        retry_delay = int(retry_after) if retry_after else RETRY_DELAY
                        logging.debug(
                            f"Rate-limited. Retrying after {retry_delay} seconds..."
                        )
                        await asyncio.sleep(retry_delay)
                        continue

                    return await response.text()

        except asyncio.TimeoutError:
            logging.debug(
                f"Request timed out while fetching data for {username}. Attempt {attempt + 1}/{MAX_RETRIES}"
            )
            break

        except aiohttp.ClientError as e:
            logging.error(
                f"Error fetching data for {username}: {e}. Attempt {attempt + 1}/{MAX_RETRIES}"
            )
            attempt += 1
            if attempt >= MAX_RETRIES:
                logging.error(f"Max retries reached for {username}.")
                break
            await asyncio.sleep(RETRY_DELAY)

    return None


# Parse the user data (extracting relevant details)
def parse_user_data(username, data):
    stats = {"Username": username}
    if data:
        soup = BeautifulSoup(data, "html.parser")
        divs = soup.find_all("div", class_="small-6 medium-3 columns text-center")
        results = {}

        for div in divs:
            value = div.find("h3").get_text(strip=True).split("\u00a0")[-1]
            label = div.find("span", class_="gras").get_text(strip=True)
            results[label] = value

        stats.update(results)

        chall = soup.find("img", src="squelettes/img/activitees.svg?1570951387")
        if chall:
            chall = chall.find_next("a")
            stats["Last Challenge"] = chall.get_text(strip=True)

        return stats

    logging.info(f"Failed to fetch or parse data for {username}.")
    return None


# Function to get users from the database
def get_users_from_db(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS rootme_users (pseudo TEXT UNIQUE)")
        conn.commit()

        cursor.execute("SELECT pseudo FROM rootme_users")
        users = [row[0] for row in cursor.fetchall()]
        return users
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return []
    finally:
        conn.close()


# Fetch and parse user data for all users in the database
async def fetch_and_parse_users():
    root_me_users = get_users_from_db(DATABASE_PATH)
    logging.info(f"Fetched {len(root_me_users)} users from the database.")
    if not root_me_users:
        logging.warning("No users found in the database.")
        return []

    all_stats = []
    for username in root_me_users:
        data = await get_user_data(username)
        if data:
            user_stats = parse_user_data(username, data)
            if user_stats:
                all_stats.append(user_stats)
        await asyncio.sleep(5)  # Add delay to avoid rate limiting
    return all_stats
