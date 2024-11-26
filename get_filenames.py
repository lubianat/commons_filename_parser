from playwright.sync_api import sync_playwright

# Output file to save scraped titles
output_file = "file_titles.txt"

# Function to save titles to a file progressively
def save_progress(titles, file_name):
    """
    Appends a list of titles to a specified file.

    Args:
        titles (list): A list of titles to save.
        file_name (str): The name of the output file.
    """
    with open(file_name, "a", encoding="utf-8") as file:
        for title in titles:
            file.write(title + "\n")

# Initialize Playwright and scrape titles
def scrape_titles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Set headless to True for a headless browser
        page = browser.new_page()

        # Base search URL
        base_url = "https://commons.wikimedia.org/w/index.php"
        search_query = {
            "limit": 500,
            "offset": 12,
            "profile": "default",
            "search": 'incategory:"Files from the Biodiversity Heritage Library" incategory:"Flickr images reviewed by FlickreviewR" -haswbstatement:P12120',
            "title": "Special:Search",
            "ns0": 1,
            "ns6": 1,
            "ns12": 1,
            "ns14": 1,
            "ns100": 1,
            "ns106": 1,
        }

        # Construct URL with query parameters
        search_url = base_url + "?" + "&".join(f"{key}={value}" for key, value in search_query.items())

        # Navigate to the URL
        page.goto(search_url)

        # Load existing progress, if any
        scraped_titles = set()
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                scraped_titles.update(line.strip() for line in file)
            print(f"Loaded {len(scraped_titles)} titles from existing progress.")
        except FileNotFoundError:
            print("No existing progress found. Starting fresh.")

        # Scrape titles from all pages
        while True:
            # Wait for the results to load
            page.wait_for_selector(".mw-search-result-heading a")

            # Extract titles
            new_titles = page.locator(".mw-search-result-heading a").all_text_contents()
            new_titles = [title for title in new_titles if title not in scraped_titles]

            # Save new titles
            if new_titles:
                save_progress(new_titles, output_file)
                scraped_titles.update(new_titles)
                print(f"Scraped {len(new_titles)} new titles. Total: {len(scraped_titles)}.")

            # Check if a "Next page" link exists
            next_button = page.locator(".mw-nextlink").first
            if next_button.count() > 0:
                next_button.click()
                page.wait_for_timeout(2000)  # Wait for the next page to load
            else:
                print("No more pages. Scraping complete.")
                break

        # Close the browser
        browser.close()

# Run the scraper
scrape_titles()
