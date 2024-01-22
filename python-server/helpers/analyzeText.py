import re


def analyze_text(text, search_string):

    text_length = len(text)
    alphanumeric_count = sum(c.isalnum() for c in text)
    unique_alphanumeric_count = len(set(c for c in text if c.isalnum()))
    occurrence_count = len(re.findall(re.escape(search_string), text, re.IGNORECASE))

    return {
        'Total Text Length': text_length,
        'Total Alphanumeric Count': alphanumeric_count,
        'Unique Alphanumeric Count': unique_alphanumeric_count,
        'Occurrences of String In Text': occurrence_count
    }
