Interactive Web Scraper with Proxy Rotation

Interactive Web Scraper with Proxy Rotation is a menu-driven command-line application built using Python. The tool allows users to scrape web pages while supporting proxy rotation, User-Agent rotation, configurable retry attempts, and exponential backoff handling for blocked requests (HTTP 403 and 429). This project demonstrates practical web scraping techniques and basic anti-block strategies commonly used in real-world automation workflows.

Features:
- Interactive CLI menu system
- Dynamic URL input
- Add and remove proxies
- Add custom User-Agent strings
- Configurable retry attempts
- Automatic retry with exponential backoff
- HTML parsing using BeautifulSoup
- Page title extraction

Technologies Used:
- Python 3.x
- requests
- beautifulsoup4
- lxml

Installation Instructions:
1. Install Python 3.x.
   Verify installation using:
   python --version

2. Install required libraries:
   pip install requests beautifulsoup4 lxml

How to Run:
1. Navigate to the project directory:
   cd path_to_project_folder

2. Run the script:
   python web_scraper.py

3. Use the interactive menu to:
   - Scrape a URL
   - Add or remove proxies
   - Add User-Agent strings
   - Set retry attempts
   - Exit the program

Project Structure:
- web_scraper.py
- README.md

Example Workflow:
1. Launch the program.
2. Optionally add proxy servers.
3. Configure retry attempts.
4. Enter a target URL.
5. View the extracted page title in the terminal.

Learning Objectives:
- Understanding HTTP requests in Python
- Configuring proxies in the requests library
- Implementing User-Agent rotation
- Handling request failures with retry logic
- Applying exponential backoff strategy
- Parsing HTML content using BeautifulSoup
- Designing interactive CLI applications

Limitations:
- Does not bypass advanced bot-detection systems.
- Does not execute JavaScript-rendered content.
- Requires valid and functional proxies for rotation to work effectively.

Future Improvements:
- Multi-threaded scraping support
- Proxy validation system
- Logging and error tracking
- Export scraped data to CSV or JSON
- Headless browser integration (e.g., Selenium)