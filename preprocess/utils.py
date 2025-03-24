import re
import unicodedata
from datetime import datetime
import difflib

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data files
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")


def remove_diacritics(value: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    )


def clean_name(value: str) -> str:
    # remove accents
    value = remove_diacritics(value)  # Yaoundé, Yaounde, yaounde
    value = value.capitalize().strip()

    if re.match(
        r"(aucun|rien |pas |non |nan$|r\s*a\s*s\s*)\s?", value, flags=re.IGNORECASE
    ):  # pas specifié, non spécifié, ras, etc.
        return "r a s"

    return re.sub(r"\(.*", "", value).strip()


def clean_date(value: str) -> str:
    re_year = r"[12]\d{3}"
    re_month = r"0?[1-9]|1[0-2]"
    re_day = r"0?[1-9]|[1-2][0-9]|3[0-1]"

    # 2024-02-01, 2023/08/04
    re_date_1 = (
        rf"(?P<years>{re_year})(/|-)(?P<months>({re_month}))\2(?P<days>({re_day}))"
    )
    # 01-02-2024, 04/08/2023
    re_date_2 = (
        rf"(?P<days>{re_day})(/|-)(?P<months>({re_month}))\2(?P<years>{re_year})"
    )

    for i in [
        re_date_1,
        re_date_2,
    ]:
        # is date?
        data = re.match(i, value)
        if not data:
            continue

        data = data.groupdict()

        date = "{years}-{months:0>2}-{days:0>2}".format(**data)

        return date

    return None


def calculate_age(birthdate):
    today = datetime.today()

    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


# Return the most similar in the list
def fix_arrondissement(value: str, possible_arrs: list[str]) -> str | None:
    if not value or value == "nan":
        return None

    # use the cutoff parameter for more precision
    return ([None] + difflib.get_close_matches(value, possible_arrs))[-1]


def sentiment_analysis(expression):
    # Basic French sentiment lexicon
    french_lexicon = {
        "pas": "positive",
        "aucune": "positive",
        "rien": "positive",
        "nan": "neutral",
    }

    # Load French stopwords
    stop_words = set(stopwords.words("french"))

    # Tokenize the sentence
    words = word_tokenize(expression, language="french")

    # Remove stopwords
    filtered_words = [
        word.lower()
        for word in words
        if word.isalnum() and word.lower() not in stop_words
    ]

    # Calculate sentiment score
    sentiment_score = 0
    for word in filtered_words:
        if word in french_lexicon:
            if french_lexicon[word] == "positive":
                sentiment_score += 2
            elif french_lexicon[word] == "neutral":
                continue
        else:
            sentiment_score -= 1

    # Determine overall sentiment
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"
