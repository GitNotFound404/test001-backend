from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import wikipedia
import re
from nltk.tokenize import sent_tokenize
from better_profanity import profanity
import nltk
import os

profanity.load_censor_words()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to your data folder
data_dir = os.path.join(script_dir, "lib_data/nltk_data")

# Add the data directory to NLTK's search path
nltk.data.path.append(data_dir)

del(nltk, os)

#use predefined more

predefined_sentences = []
with open('predefined.txt', 'r') as predefined_file:
    predefined_sentences = predefined_file.read().split('\n')

topics_list = []
with open('topics.txt', 'r') as topics_txt:
        topics_list = topics_txt.read().split('\n')

nicknames = ["dude","guy","bob","thanos","idiot","boi","stupid"]

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({
        "name": "dude",
        "age": 420,
        "nickname": "guy"
    })

@app.route("/api/random_nick")
def get_random_nickname():
    return jsonify({
        "id": random.randint(1000, 9999),
        "nickname": random.choice(nicknames)
    })

@app.route("/api/get-sentences-on-random-topic/")
def get_random_topic_sentences():
    value = [None, None, "sentence"]
    while (not value[0]):
        random_topic = topics_list[random.randint(0, len(topics_list)-1)].title()
        print("Topic:", random_topic)
        custom_topic = request.args.get('topic', default=random_topic)
        del(topics_txt, topics_list, random_topic)
        value = get_all_sentences(custom_topic)
        print(value)
    return jsonify(value)

@app.route("/api/get-predefined-sentences-list/")
def get_predefined_list():
    return predefined_sentences

# Make sure you have downloaded the NLTK 'punkt' tokenizer:
# nltk.download('punkt')

def get_all_sentences(topic):
    """
    Fetches all clean, and meaningful sentences on a given topic
    from Wikipedia for testing purposes.
    """
    try:
        # We'll use a larger search result set to increase our chances.
        print("1. Getting Results")
        search_results = wikipedia.search(topic, results=7)
        print("2. Got Results")
        if not search_results:
            return None, "No results found for that topic. Please try another."

        easy_sentences = []
        for page_title in search_results:
            print("3.1. Loop Results")
            try:
                print("3.2. Getting page")
                page = wikipedia.page(page_title, auto_suggest=True, redirect=True)
                print("3.3. Got page")
                raw_text = page.content

                # Step 1: Clean the raw text
                clean_text = re.sub(r'\(.*?\)|\[.*?\]', '', raw_text)
                clean_text = re.sub(r'==.*?==', '', clean_text, flags=re.DOTALL)
                clean_text = re.sub(r'\n', ' ', clean_text)
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                print("3.4. Tokenizing")
                sentences = sent_tokenize(clean_text)
                print("3.5. Tokenized")

                # Step 2: Filter the sentences for simplicity and meaning
                for sentence in sentences:
                    print("3.6. Looping through sentences with checks")
                    sentence = sentence.strip()

                    #if (profanity.contains_profanity(sentence)):
                    #    print("Profanity detected, skipping to next sentence.")
                    #    continue

                    # Rule for Numbers: Allow a single 4-digit number (like a year), but no others.
                    numbers = re.findall(r'\d+', sentence)

                    # If the sentence has more than one number, discard it.
                    if len(numbers) > 1:
                        continue

                    # If there is exactly one number, check if it's 4 digits long.
                    if len(numbers) == 1 and not re.search(r'^\d{4}$', numbers[0]):
                        continue

                    if '...' in sentence:
                        continue
                    
                    # Rule 2: Remove sentences that match a pattern of [letter/number][symbol][letter/number].
                    # This targets things like "a:1", "b-2", or "c.3"
                    if re.search(r'(\s[a-zA-Z0-9][:\-/\.][a-zA-Z0-9])|([a-zA-Z0-9][:\-/\.][a-zA-Z0-9]\s)', sentence):
                        continue

                    # Rule 3: Remove sentences with a letter and a number next to each other.
                    # This catches patterns like "1a", "a5", or "Qh41b".
                    if re.search(r'\w*\d+[a-zA-Z]+|\w*[a-zA-Z]+\d+', sentence):
                        continue

                    # Rule 4: Remove sentences that have content after the final period.
                    if re.search(r'\.\s*\S', sentence):
                        continue

                    # Rule 6: Filter out sentences that are fully enclosed in parentheses.
                    if re.match(r'^\(.*\)$', sentence):
                        continue

                    # Rule 5: Remove sentences with more than one comma.
                    if sentence.count(',') > 1:
                        continue

                    # Rule 0: Handle unwanted leading characters like = or *.
                    if re.match(r'^[=|\*]', sentence):
                        if sentence.startswith('= '):
                            sentence = sentence[2:].strip()
                        else:
                            continue
                            
                    # Rule 1: Use a more flexible word count for a wider range of sentences.
                    word_count = len(sentence.split())
                    if not (4 < word_count < 15):
                        continue
                    
                    # Rule 2: Filter out sentences containing specific unwanted symbols.
                    if re.search(r'[:|~`@=*;\\⊕ß§ſ†‡¶·"()[\]{}/]', sentence):
                        continue
                        
                    # Rule 3: Filter out sentences with en-dashes or em-dashes.
                    if re.search(r'[–—]', sentence):
                        continue

                    # Rule 4: Filter out short sentences that are likely references.
                    if re.search(r'"[^"]+"', sentence):
                        continue
                    
                    # Rule 5: Ensure sentences start with a capital letter.
                    if re.match(r'^[a-z]', sentence):
                        continue

                    # Rule 6: Filter out sentences that start or end with a citation-like term.
                    if re.search(r'^(?:i\.e\.|e\.g\.|etc\.|et\sal\.)\s*|\s*(?:i\.e\.|e\.g\.|etc\.|et\sal\.)$', sentence, re.IGNORECASE):
                        continue

                    # Rule 7: Filter out glossary or list-like sentences.
                    if re.search(r'^(See\b|Also|But)', sentence, re.IGNORECASE):
                        continue
                    if re.match(r'^[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s', sentence):
                        continue
                    if re.search(r'^\d+\.\s?[a-z]\.?\s?', sentence):
                        continue

                    # Rule 8: Filter out sentences with too many numbers.
                    if sum(c.isdigit() for c in sentence) > 3:
                        continue

                    if re.search(r'^(As of|All rights reserved|ISBN|ISSN|copyright)', sentence, re.IGNORECASE):
                        continue
                    
                    # Rule 9: Filter out sentences that start with a linking adverb.
                    linking_adverbs = r'^(However|Conversely|Similarly|Therefore|Thus|Hence|Moreover|Furthermore|In addition|For example|As an example)\b'
                    if re.match(linking_adverbs, sentence, re.IGNORECASE):
                        continue

                    # Final step: If the sentence passes all filters, remove the trailing period and trim it.
                    if sentence.endswith('.'):
                        sentence = sentence[:-1]
                    
                    #if ((not (32 <= ord(c) <= 122)) for c in sentence):
                    #    continue

                    bad_symbols = False
                    for chr in sentence:
                        if not (32 <= ord(chr) <= 122):
                            bad_symbols = True
                    
                    if bad_symbols:
                        continue

                    easy_sentences.append(sentence.strip())
            
            except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                continue

        if easy_sentences:
            print("4. Done, returning sentences")
            return [easy_sentences, None, page_title] #Page title instead of topic.
        else:
            return None, "Could not find suitable sentences on this topic. Try another."

    except Exception as e:
        return None, f"An unexpected error occurred: {e}"


#if (__name__ == "__main__"):
#    app.run(host="0.0.0.0", port=10000) # For testing purposes, remove this in final build and instead use gunicorn.
