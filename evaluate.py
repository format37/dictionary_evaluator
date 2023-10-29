import pandas as pd
from collections import Counter
import string
import matplotlib.pyplot as plt
import os
import glob


def plot_word_frequency_modified(df):

    records_count_limit = 20

    # Filter words spoken by user
    words_user = df[df['User_Frequency'] > 0]

    # Filter words exclusively spoken by the user
    words_user_only = df[(df['User_Frequency'] > 0) & (df['Assistant_Frequency'] == 0)]

    # Filter words exclusively spoken by the assistant
    words_assistant_only = df[(df['User_Frequency'] == 0) & (df['Assistant_Frequency'] > 0)]

    # Sort the data by frequency
    words_user = words_user.sort_values(by='User_Frequency', ascending=True)
    words_user_only_sorted = words_user_only.sort_values(by='User_Frequency', ascending=True)
    words_assistant_only_sorted = words_assistant_only.sort_values(by='Assistant_Frequency', ascending=True)    

    # Function to plot horizontal bar chart
    def plot_horizontal_bar(df, title, xlabel, ylabel, color):

        # Limit the number of records
        df = df.tail(records_count_limit)

        plt.figure(figsize=(10, len(df) // 2))
        plt.barh(df[ylabel], df[xlabel], color=color)

        # Add grid
        plt.grid(axis='x')
        
        # Add numbers line to the top
        plt.tick_params(axis='x', which='both', bottom=True, top=True, labeltop=True)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.savefig('data/output/' + title + '.png')

    plot_horizontal_bar(words_user, 'Words Spoken by User', 'User_Frequency', 'Word', 'blue')
    plot_horizontal_bar(words_user_only_sorted, 'Words Exclusively Spoken by User', 'User_Frequency', 'Word', 'blue')
    plot_horizontal_bar(words_assistant_only_sorted, 'Words Exclusively Spoken by Assistant', 'Assistant_Frequency', 'Word', 'green')


def clean_and_tokenize(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text.split()


def word_frequency(text):
    words = clean_and_tokenize(text)
    return Counter(words)


def progress():
    # Function to tokenize text
    def tokenize(text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation)) 
        return text.split()

    # Initialize dictionary to store word sets
    assistant_words = {}  

    # Initialize lists to store data
    
    filenames = []
    new_words = []

    # Loop through assistant conversation files sorted
    for f in sorted(glob.glob('data/assistant/*.txt')):

        # Load assistant text 
        with open(f) as file:
            assistant_text = file.read()
            
        # Load corresponding user text
        user_file = f.replace('assistant', 'user')
        with open(user_file) as file:
            user_text = file.read()
        
        # Tokenize texts
        assistant_tokens = tokenize(assistant_text) 
        user_tokens = tokenize(user_text)
        
        # Create word frequency counters
        assistant_freq = Counter(assistant_tokens)
        user_freq = Counter(user_tokens)
        
        # Get words only used by assistant
        only_assistant = set([w for w in assistant_freq if w not in user_freq])

        # Get all words that was used by user
        all_user = set([w for w in user_freq if w in assistant_freq])
        
        # Store in dictionary
        assistant_words[user_file] = only_assistant

        # Calculate how many words was used by user from the current and pervious assistant words
        user_progress = 0
        for key, value in assistant_words.items():
            user_progress += len(value.intersection(all_user))
            # Print which words was used by user from the current and pervious assistant words
            
            print(f, len(value.intersection(all_user)), "words reused by user:")
            print(f, value.intersection(all_user), '\n')
            new_user_words = value.intersection(all_user)        
            # Append to lists
            new_words.append(len(new_user_words))
        filenames.append(f)

        #print count of words only used by assistant
        print(f, len(only_assistant), user_progress, 'words only used by assistant')

        # Create bar chart 
        plt.figure()
        plt.bar(range(len(new_words)), new_words)

        # Rotate x-axis labels
        plt.xticks(range(len(filenames)), labels=filenames, rotation=75) 

        # Label axes
        plt.xlabel('Conversation File')
        plt.ylabel('New Words Used')

        # Save figure
        plt.tight_layout()
        plt.savefig('data/output/user_progress.png')

def frequency():
    # Initialize empty strings to hold texts
    user_text = ''
    assistant_text = ''

    # Read user texts from multiple files
    user_files = os.listdir('data/user/')
    for file in user_files:
        with open(f'data/user/{file}', 'r') as f:
            user_text += ' ' + f.read()

    # Read assistant texts from multiple files
    assistant_files = os.listdir('data/assistant/')
    for file in assistant_files:
        with open(f'data/assistant/{file}', 'r') as f:
            assistant_text += ' ' + f.read()

    user_word_freq = word_frequency(user_text)
    assistant_word_freq = word_frequency(assistant_text)

    # Create DataFrame
    df = pd.DataFrame(list(set(list(user_word_freq.keys()) + list(assistant_word_freq.keys()))), columns=['Word'])

    # Populate DataFrame with frequencies
    df['User_Frequency'] = df['Word'].apply(lambda x: user_word_freq.get(x, 0))
    df['Assistant_Frequency'] = df['Word'].apply(lambda x: assistant_word_freq.get(x, 0))

    # Sort DataFrame by Word column
    df = df.sort_values('Word')

    # Save DataFrame to CSV
    df.to_csv('data/output/word_frequency_table.csv', index=False)

    plot_word_frequency_modified(df)

    # Print the number of words that persist in the user's text    
    print(df[df['User_Frequency'] > 0].shape[0] , "- Count of overall words that persist in the user's text")
    print(df[df['Assistant_Frequency'] > 0].shape[0], "- Count of overall words that persist in the assistant's text")
    print(df[(df['User_Frequency'] > 0) & (df['Assistant_Frequency'] == 0)].shape[0], "- Count of words that persist only in the user's text")
    print(df[(df['User_Frequency'] == 0) & (df['Assistant_Frequency'] > 0)].shape[0], "- Count of words that persist only in the assistant's text")

    # Write line by line in a file named assistant_only.txt sorted by frequency
    with open('data/output/assistant_only_sorted.txt', 'w') as f:
        for word in df[(df['User_Frequency'] == 0) & (df['Assistant_Frequency'] > 0)].sort_values(by='Assistant_Frequency', ascending=False)['Word'].tolist():
            f.write(word + '\n')

    # Write line by line in a file named user_only.txt sorted by frequency
    with open('data/output/user_only_sorted.txt', 'w') as f:
        for word in df[(df['User_Frequency'] > 0) & (df['Assistant_Frequency'] == 0)].sort_values(by='User_Frequency', ascending=False)['Word'].tolist():
            f.write(word + '\n')

    # Write a user's dictionary sorted by frequency desc to a file named user_dictionary.txt
    with open('data/output/user_dictionary.txt', 'w') as f:
        for word in df[df['User_Frequency'] > 0].sort_values(by='User_Frequency', ascending=False)['Word'].tolist():
            f.write(word + '\n')

    # Write an assistant's dictionary sorted by frequency desc to a file named assistant_dictionary.txt
    with open('data/output/assistant_dictionary.txt', 'w') as f:
        for word in df[df['Assistant_Frequency'] > 0].sort_values(by='Assistant_Frequency', ascending=False)['Word'].tolist():
            f.write(word + '\n')


def main():
    frequency()
    progress()


if __name__ == '__main__':
    main()
