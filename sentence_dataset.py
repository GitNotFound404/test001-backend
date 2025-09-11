def getSentences():
    sentences = []
    
    with open('sentences.txt', 'r', encoding='utf-8') as sentences_file:
        sentences = sentences_file.read().split('\n')

    return sentences
