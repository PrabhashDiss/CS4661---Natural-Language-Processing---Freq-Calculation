import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import zipfile
import os

source_file = '21193_Sinhala.txt'
index_number = '200144X'

# Read the text file
with open(source_file, 'r', encoding='utf-8') as file:
    text = file.read()

# Calculate word frequencies
words = text.split()
word_freq = Counter(words)

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

# Plot rank vs frequency graph
plt.figure(figsize=(10, 6))
plt.plot(frq_df['Rank'], frq_df['Freq'], marker='o')
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.title('Rank vs Frequency')
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