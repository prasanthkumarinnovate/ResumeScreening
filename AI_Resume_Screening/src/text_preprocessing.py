import re
import string


def preprocess(text):

    # convert to lowercase
    text = text.lower()

    # remove numbers
    text = re.sub(r"\d+", " ", text)

    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()