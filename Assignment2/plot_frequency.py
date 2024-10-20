import os
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter

# Directory containing the downloaded HTML files
input_dir = "mark_six_results_html"

# Function to extract ball numbers from an HTML file
def extract_balls_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # This regular expression matches numbers between 1 and 49 (ball numbers)
        ball_pattern = re.compile(r'\b([1-9]|[1-4][0-9])\b')

        # Find all the text that could contain ball numbers
        text = soup.get_text()

        # Extract all matches of the ball pattern
        balls = ball_pattern.findall(text)

        # Convert extracted numbers to integers
        return [int(ball) for ball in balls]

# Collect all ball numbers from every file
all_balls = []

# Loop through all HTML files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(input_dir, filename)
        balls = extract_balls_from_html(file_path)
        all_balls.extend(balls)

# Count the frequency of each ball number
ball_counter = Counter(all_balls)

# Separate the ball numbers and their frequencies for plotting
balls = list(ball_counter.keys())
frequencies = list(ball_counter.values())

# Sort the balls in ascending order for better visualization
balls, frequencies = zip(*sorted(zip(balls, frequencies)))

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(balls, frequencies, color='skyblue')

# Add labels and title
plt.title('Mark Six Ball Frequency Over Multiple Years', fontsize=16)
plt.xlabel('Ball Number', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# Display the plot
plt.xticks(balls)  # Ensure all ball numbers appear on the x-axis
plt.show()
