def getData():
    predefined_sentences = []
    with open('predefined.txt', 'r') as predefined_file:
        predefined_sentences = predefined_file.read().split('\n')

    topics_list = []
    with open('topics.txt', 'r') as topics_txt:
            topics_list = topics_txt.read().split('\n')

    return predefined_sentences, topics_list
