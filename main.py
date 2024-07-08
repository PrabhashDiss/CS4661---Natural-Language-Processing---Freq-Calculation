import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import zipfile
import os
import re

source_file = '21193_Sinhala.txt'
index_number = '200144X'

# Function to filter non-words
def is_sinhala_word(word):
    # Sinhala Unicode block ranges from 0D80 to 0DFF
    sinhala_char_range = re.compile(r'^[\u0D80-\u0DFF]+$')
    return sinhala_char_range.match(word)

# Read the text file
with open(source_file, 'r', encoding='utf-8') as file:
    text = file.read()

# Split text into words
words = text.split()

# Filter words to include only Sinhala words
sinhala_words = []
non_sinhala_words = []

for word in words:
    if is_sinhala_word(word):
        sinhala_words.append(word)
    else:
        non_sinhala_words.append(word)

# Write non-Sinhala words to a separate file
with open('non_sinhala_words.txt', 'w', encoding='utf-8') as file:
    for word in non_sinhala_words:
        file.write(f"{word}\n")

# Calculate word frequencies
word_freq = Counter(sinhala_words)

# Save word frequencies to Frq.csv
frq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Freq'])
frq_df.to_csv('Frq.csv', index=False)

# Calculate frequency of frequencies
freq_of_freq = Counter(word_freq.values())

# Save frequency of frequencies to FrFr.csv
frfr_df = pd.DataFrame(freq_of_freq.items(), columns=['Freq', 'FreqOfFreq'])
frfr_df.to_csv('FrFr.csv', index=False)

# Rank the words based on their frequencies
frq_df['Rank'] = frq_df['Freq'].rank(method='max', ascending=False).astype(int)
frq_df = frq_df.sort_values(by='Rank')

# Save ranks to Rank.csv
frq_df.to_csv('Rank.csv', index=False)

# Plot rank vs frequency graph with logarithmic scales
plt.figure(figsize=(10, 6))
plt.plot(frq_df['Rank'], frq_df['Freq'], marker='o', linestyle='None')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.title('Rank vs Frequency (Log-Log Scale)')
plt.grid(True)
plt.savefig('Graph.png')

# Create a zip file
zip_filename = f"{index_number}.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(source_file)
    zipf.write('Frq.csv')
    zipf.write('FrFr.csv')
    zipf.write('Rank.csv')
    zipf.write('Graph.png')

print(f"{zip_filename} created successfully.")
