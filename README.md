# blog-authorship-corpus-analysis
Script for analyzing a corpus of blogs. Looking into the corpus from NLP perspective

# How to create Docker Image
Run this command in root of the project
```
docker build -t blog-authorship-corpus-analysis .
```
# How to start the Docker Image
```
docker run --rm blog-authorship-corpus-analysis
```

# 🧠 Script Overview
This script performs three main tasks:

Most Common Words
- It analyzes a collection of blog texts to identify the 10 most frequently occurring words.

Word Similarity
- It computes and displays the 50 most similar pairs of words based on their embeddings or context.

Dollar Amount Extraction
- It calculates the total sum of all dollar amounts mentioned in the texts.

After completing these tasks, a Streamlit web app is launched to display the results along with visualizations for additional tasks.
