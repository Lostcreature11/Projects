
import requests
import random
import time
from bs4 import BeautifulSoup


proxies = []
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

retries = 5



def scrape(url):
    global proxies, user_agents, retries

    for attempt in range(retries):
        proxy = random.choice(proxies) if proxies else None
        headers = {"User-Agent": random.choice(user_agents)}

        print(f"\nAttempt {attempt + 1}/{retries}")
        if proxy:
            print("Using proxy:", proxy)

        try:
            response = requests.get(
                url,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=10
            )

            print("Status Code:", response.status_code)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")
                title = soup.title.text.strip() if soup.title else "No title found"
                print("\nPage Title:", title)
                return

            elif response.status_code in [403, 429]:
                wait_time = 2 ** attempt
                print(f"Blocked. Waiting {wait_time} seconds...")
                time.sleep(wait_time)

        except requests.RequestException as e:
            wait_time = 2 ** attempt
            print("Request failed:", e)
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    print("\nFailed after all retries.")



def add_proxy():
    proxy = input("Enter proxy (http://user:pass@host:port): ").strip()
    if proxy:
        proxies.append(proxy)
        print("Proxy added.")


def remove_proxy():
    if not proxies:
        print("No proxies available.")
        return

    for i, p in enumerate(proxies):
        print(f"{i + 1}. {p}")

    choice = input("Select proxy number to remove: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(proxies):
            removed = proxies.pop(index)
            print("Removed:", removed)


def add_user_agent():
    ua = input("Enter User-Agent string: ").strip()
    if ua:
        user_agents.append(ua)
        print("User-Agent added.")


def set_retries():
    global retries
    value = input("Enter retry attempts: ").strip()
    if value.isdigit():
        retries = int(value)
        print("Retries updated.")



def main():
    while True:
        print("\n==== Interactive Web Scraper ====")
        print("1. Scrape a URL")
        print("2. Add Proxy")
        print("3. Remove Proxy")
        print("4. Add User-Agent")
        print("5. Set Retry Attempts")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            url = input("Enter URL: ").strip()
            scrape(url)

        elif choice == "2":
            add_proxy()

        elif choice == "3":
            remove_proxy()

        elif choice == "4":
            add_user_agent()

        elif choice == "5":
            set_retries()

        elif choice == "6":
            print("Exiting scraper.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()