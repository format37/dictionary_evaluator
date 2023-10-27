
import pandas as pd
from collections import Counter
import string
import matplotlib.pyplot as plt

def plot_word_frequency(csv_file_path):
    # Load the CSV file into a DataFrame
    word_frequency_df = pd.read_csv(csv_file_path)
    
    # Filter words exclusively spoken by the user
    words_user_only = word_frequency_df[(word_frequency_df['User_Frequency'] > 0) & (word_frequency_df['Assistant_Frequency'] == 0)]
    
    # Filter words exclusively spoken by the assistant
    words_assistant_only = word_frequency_df[(word_frequency_df['User_Frequency'] == 0) & (word_frequency_df['Assistant_Frequency'] > 0)]
    
    # Sort the data by frequency
    words_user_only_sorted = words_user_only.sort_values(by='User_Frequency', ascending=True)
    words_assistant_only_sorted = words_assistant_only.sort_values(by='Assistant_Frequency', ascending=True)
    
    # Function to plot horizontal bar chart
    def plot_horizontal_bar(df, title, xlabel, ylabel, color):
        plt.figure(figsize=(10, len(df) // 2))
        plt.barh(df[ylabel], df[xlabel], color=color)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        # plt.show()
        # Save the plot as a PNG image
        plt.savefig(title + '.png')
    
    # Plot for words exclusively spoken by the user
    plot_horizontal_bar(words_user_only_sorted, 'Words Exclusively Spoken by User', 'User_Frequency', 'Word', 'blue')
    
    # Plot for words exclusively spoken by the assistant
    plot_horizontal_bar(words_assistant_only_sorted, 'Words Exclusively Spoken by Assistant', 'Assistant_Frequency', 'Word', 'green')


# Function to clean and tokenize the text
def clean_and_tokenize(text):
    # Remove punctuation and convert to lowercase
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text.split()

# Function to count frequency of each word in a given text
def word_frequency(text):
    words = clean_and_tokenize(text)
    return Counter(words)

# Replace these example texts with your actual texts
# user_text = 'Your user text here...'
# read from user.txt
with open('user.txt', 'r') as f:
    user_text = f.read()
# assistant_text = 'Your assistant text here...'
# read from assistant.txt
with open('assistant.txt', 'r') as f:
    assistant_text = f.read()

# Count word frequencies in each text
user_word_freq = word_frequency(user_text)
assistant_word_freq = word_frequency(assistant_text)

# Create a DataFrame to hold the word frequencies
df = pd.DataFrame(list(set(list(user_word_freq.keys()) + list(assistant_word_freq.keys()))), columns=['Word'])

# Populate the DataFrame with the frequencies
df['User_Frequency'] = df['Word'].apply(lambda x: user_word_freq.get(x, 0))
df['Assistant_Frequency'] = df['Word'].apply(lambda x: assistant_word_freq.get(x, 0))

# Sort the DataFrame by the Word column
df = df.sort_values('Word')

# Save the DataFrame to a CSV file
df.to_csv('word_frequency_table.csv', index=False)

plot_word_frequency('word_frequency_table.csv')

# Print the count of overall words that persist in the user's text
print("Count of overall words that persist in the user's text:", df[df['User_Frequency'] > 0].shape[0])

# Print the count of words that persist only in the assistant's text
print("Count of words that persist only in the assistant's text:", df[(df['User_Frequency'] == 0) & (df['Assistant_Frequency'] > 0)].shape[0])

# Write line by line in a file named assistant_only.txt sorted by frequency
with open('assistant_only_sorted.txt', 'w') as f:
    for word in df[(df['User_Frequency'] == 0) & (df['Assistant_Frequency'] > 0)].sort_values(by='Assistant_Frequency', ascending=False)['Word'].tolist():
        f.write(word + '\n')