 Async GitHub API Wrapper Library

 Overview

Async GitHub API Wrapper is a production-ready Python library that provides an asynchronous interface to the GitHub REST API using aiohttp. The library is designed with clean architecture principles, built-in rate limiting, automatic pagination handling, structured error management, and developer-friendly abstractions.

It exposes a typed, resource-oriented client class that simplifies interaction with GitHub resources such as users and repositories while handling real-world API constraints like rate limits and transient failures.

---

 Features

- Fully asynchronous API client using asyncio and aiohttp
- Class-based client architecture (GitHubAPI)
- Async context manager support for proper session handling
- In-memory token-bucket style rate limiter
- Automatic handling of GitHub rate limit headers
- Retry-after logic for 429 responses
- Automatic retries with exponential backoff for 5xx errors
- Async generator-based pagination
- Custom exception hierarchy for structured error handling
- Type hints for all public methods
- Interactive CLI demonstration included

---

 Technologies Used

- Python 3.8+
- asyncio
- aiohttp
- Type hints (typing module)

---

Installation

1. Install Python 3.8 or higher.
2. Install required dependency:

   pip install aiohttp

---

How to Run (Interactive Demo)

Navigate to the project directory and run:

   python async_github.py

The interactive menu allows you to:
1. Fetch a GitHub user profile
2. Stream a user's repositories with automatic pagination
3. Exit the program

You may provide a GitHub Personal Access Token for higher rate limits, or press Enter to use unauthenticated public access.

---

 Architecture Overview

The library is structured around four major components:

1. GitHubAPI Client  
   - Central class managing HTTP requests  
   - Maintains a shared aiohttp session  
   - Exposes resource-oriented public methods  

2. RateLimiter  
   - Implements in-memory token bucket behavior  
   - Controls maximum API calls per time window  
   - Prevents exceeding GitHub’s rate limits  

3. Pagination System  
   - Uses async generators  
   - Streams paginated responses page by page  
   - Avoids loading large datasets into memory  

4. Error Hierarchy  
   - APIError (base exception)  
   - NotFoundError (404)  
   - RateLimitError (rate limit exceeded)  
   - ServerError (5xx failures)  

---
Example Usage (Library Mode)

```python
import asyncio
from async_github import GitHubAPI

async def main():
    async with GitHubAPI("your_token_here") as api:
        user = await api.get_user("torvalds")
        print(user["name"])

        async for repo in api.get_repositories("torvalds"):
            print(repo["name"])

asyncio.run(main())