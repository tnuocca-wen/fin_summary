import re


def add_spaces_after_punctuation(text):
    punctuation = ['.', ',']
    modified_text = ""

    for char in text:
        if char in punctuation:
            modified_text = modified_text.rstrip()  # Remove spaces before punctuation
            modified_text += char
            if modified_text and modified_text[-1] != ' ':
                modified_text += ' '
        else:
            modified_text += char

    return modified_text.strip()  # Remove leading/trailing spaces


def split_into_sentences_custom(text):
    # Remove spaces around commas in the entire string
    # cleaned_text = re.sub(r'\s*,\s*', ',', text)
    cleaned_text = add_spaces_after_punctuation(text)
    sentences = []
    current_sentence = ""
    words = cleaned_text.split()

    for word in words:
        current_sentence += word + " "
        clean_word = word.replace(',', '')  # Remove commas
        if clean_word[-1] == '.' and len(clean_word) > 7 and not clean_word[:-1].isdigit():
            sentences.append(current_sentence.strip())
            current_sentence = ""

    # Add the last sentence (if any)
    if current_sentence:
        sentences.append(current_sentence.strip())

    return sentences
