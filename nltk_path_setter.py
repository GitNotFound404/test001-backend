def setPath():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to your data folder
    data_dir = os.path.join(script_dir, "lib_data/nltk_data")

    # Add the data directory to NLTK's search path
    nltk.data.path.append(data_dir)

    del(nltk, os)
