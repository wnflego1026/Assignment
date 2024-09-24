import os
import requests

# Create a directory to store the downloaded HTML files
output_dir = "mark_six_results_html"
os.makedirs(output_dir, exist_ok=True)

# Base URL pattern for the results
base_url = "https://lottery.hk/en/mark-six/results/{}"

# Range of years for which you want to download the results
years = range(1993, 2025)  # Modify the range as needed

# Function to download the HTML for a given year
def download_mark_six_results(year):
    url = base_url.format(year)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Save the HTML content to a file
        file_path = os.path.join(output_dir, f"mark_six_{year}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Downloaded results for {year} and saved to {file_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for year {year}: {http_err}")
    except Exception as err:
        print(f"Error occurred for year {year}: {err}")

# Loop over the years and download the results for each year
for year in years:
    download_mark_six_results(year)

print("All downloads completed.")
