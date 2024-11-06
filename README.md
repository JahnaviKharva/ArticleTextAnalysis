# ArticleTextAnalysis

Project Overview
ArticleTextAnalysis is a Python project for performing detailed textual analysis on extracted article text. It computes a range of linguistic and sentiment-based metrics, including positive/negative scores, polarity, subjectivity, sentence complexity, and readability scores, based on pre-defined dictionaries and stopwords lists. The project is designed to analyze the text content from various sources, providing insightful metrics that can be used for data analysis or sentiment-based reporting.

Features
Text Analysis: Computes sentiment scores (positive, negative, polarity, and subjectivity).
Readability Metrics: Calculates the FOG index, average sentence length, complex word count, and syllables per word.
Word and Sentence Analysis: Provides word count, personal pronoun count, and average word length.
Customizable Dictionaries: Uses custom stopwords, positive, and negative word lists for more tailored analysis.
Installation
To get started, clone the repository and set up the required packages.

Clone the Repository


git clone https://github.com/JahnaviKharva/ArticleTextAnalysis
cd ArticleTextAnalysis
Install Dependencies Make sure you have Python installed. You can install the required packages using:



Download Required NLTK Resources Run the following Python commands once to download necessary NLTK data:

Python
import nltk
nltk.download('punkt')
nltk.download('stopwords')


Project Structure
Input.xlsx: Excel file containing URLs and IDs of articles to be analyzed.
extracted_articles/: Folder containing the text files of articles extracted for analysis.
Output Data Structure.xlsx: Template file for the output structure.
StopWords/: Folder with custom stopwords lists used in the analysis.
MasterDictionary/: Folder with positive and negative words list.
output.xlsx: Generated output file with the analyzed metrics for each article.


Usage
Prepare the Input Files

Place article text files in the extracted_articles/ folder.
Ensure Input.xlsx contains the necessary URLs and IDs.
Ensure that StopWords and MasterDictionary folders contain relevant files.
Run the Analysis Run the main script to process the text and compute metrics:


python analysis.py
The results will be saved to output.xlsx.

Output
The output file, output.xlsx, contains the following fields:

Sentiment Scores: POSITIVE SCORE, NEGATIVE SCORE, POLARITY SCORE, SUBJECTIVITY SCORE.
Readability Metrics: FOG INDEX, AVG SENTENCE LENGTH, PERCENTAGE OF COMPLEX WORDS.
Word Analysis: WORD COUNT, SYLLABLE PER WORD, AVG WORD LENGTH.
Pronoun Count: Count of personal pronouns used in the text.
Customization
You can customize the analysis by modifying the stopwords and master dictionaries:

Stopwords: Add or remove words from the StopWords text files.
Positive/Negative Words: Update positive-words.txt and negative-words.txt files in the MasterDictionary folder to reflect your needs.
Contributing
Contributions are welcome! If you want to suggest improvements or fix issues, feel free to open a pull request.








