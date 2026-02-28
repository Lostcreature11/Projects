

import aiohttp
import asyncio
import time
from typing import AsyncGenerator, Optional, Dict, Any


# -----------------------------
# Custom Exceptions
# -----------------------------

class APIError(Exception):
    """Base API exception"""


class NotFoundError(APIError):
    """Raised when resource not found"""


class RateLimitError(APIError):
    """Raised when rate limit exceeded"""


class ServerError(APIError):
    """Raised for 5xx server errors"""



class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = 0
        self.reset_time = time.time() + period

    async def acquire(self):
        current_time = time.time()

        if current_time > self.reset_time:
            self.calls = 0
            self.reset_time = current_time + self.period

        if self.calls >= self.max_calls:
            wait_time = self.reset_time - current_time
            await asyncio.sleep(max(0, wait_time))
            self.calls = 0
            self.reset_time = time.time() + self.period

        self.calls += 1



class GitHubAPI:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = RateLimiter(5000, 3600)

    async def __aenter__(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/{endpoint}"

        for attempt in range(3):
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    await self._handle_rate_headers(response)

                    if response.status == 404:
                        raise NotFoundError("Resource not found")

                    if response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        await asyncio.sleep(retry_after)
                        continue

                    if 500 <= response.status < 600:
                        await asyncio.sleep(2 ** attempt)
                        continue

                    response.raise_for_status()
                    return await response.json()

            except aiohttp.ClientError as e:
                if attempt == 2:
                    raise APIError(f"Request failed: {e}")
                await asyncio.sleep(2 ** attempt)

        raise ServerError("Max retries exceeded")

    async def _handle_rate_headers(self, response):
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining is not None and int(remaining) == 0:
            wait_time = int(reset) - int(time.time())
            if wait_time > 0:
                raise RateLimitError(f"Rate limit exceeded. Retry in {wait_time}s")

    

    async def get_user(self, username: str) -> Dict[str, Any]:
        """Get user profile"""
        return await self._request("GET", f"users/{username}")

    async def get_repositories(self, username: str, per_page: int = 100) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream user repositories with pagination"""
        page = 1

        while True:
            data = await self._request(
                "GET",
                f"users/{username}/repos",
                params={"page": page, "per_page": per_page}
            )

            if not data:
                break

            for repo in data:
                yield repo

            page += 1



async def interactive_menu():
    token = input("Enter GitHub token (or press Enter for public access): ").strip()
    token = token if token else None

    async with GitHubAPI(token) as api:
        while True:
            print("\n==== GitHub Async Client ====")
            print("1. Get User Profile")
            print("2. List User Repositories")
            print("3. Exit")

            choice = input("Select option: ").strip()

            if choice == "1":
                username = input("Enter username: ").strip()
                try:
                    user = await api.get_user(username)
                    print("\nName:", user.get("name"))
                    print("Public Repos:", user.get("public_repos"))
                    print("Followers:", user.get("followers"))
                except APIError as e:
                    print("Error:", e)

            elif choice == "2":
                username = input("Enter username: ").strip()
                try:
                    async for repo in api.get_repositories(username):
                        print("-", repo.get("name"))
                except APIError as e:
                    print("Error:", e)

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid option.")


if __name__ == "__main__":
    asyncio.run(interactive_menu())