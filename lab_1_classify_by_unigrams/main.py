"""
Lab 1.

Language detection
"""
# pylint:disable=too-many-locals, unused-argument, unused-variable


def tokenize(text: str) -> list[str] | None:
    """
    Split a text into tokens.

    Convert the tokens into lowercase, remove punctuation, digits and other symbols

    Args:
        text (str): A text

    Returns:
        list[str] | None: A list of lower-cased tokens without punctuation

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(text, str):
        return None
    text = text.lower()
    cleaned_text = []
    for i in text:
        if i.isalpha():
            cleaned_text.append(i)
    return cleaned_text


def calculate_frequencies(tokens: list[str] | None) -> dict[str, float] | None:
    """
    Calculate frequencies of given tokens.

    Args:
        tokens (list[str] | None): A list of tokens

    Returns:
        dict[str, float] | None: A dictionary with frequencies

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(tokens, list):
        return None

    length = len(tokens)
    freq_dictionary = {}

    for letter in tokens:
        if not isinstance(letter, str):
            return None
        if letter not in freq_dictionary:
            freq_dictionary[letter] = 0
        freq_dictionary[letter] += 1

    for letter in freq_dictionary:
        freq_dictionary[letter] = freq_dictionary[letter] / length
    return freq_dictionary


def create_language_profile(language: str, text: str) -> dict[str, str | dict[str, float]] | None:
    """
    Create a language profile.

    Args:
        language (str): A language
        text (str): A text

    Returns:
        dict[str, str | dict[str, float]] | None: A dictionary with two keys – name, freq

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(language, str) or not isinstance(text, str):
        return None
    language_profile_dictionary = {}
    language_profile_dictionary['name'] = language
    language_profile_dictionary['freq'] = calculate_frequencies(tokenize(text))
    return language_profile_dictionary


def calculate_mse(predicted: list, actual: list) -> float | None:
    """
    Calculate mean squared error between predicted and actual values.

    Args:
        predicted (list): A list of predicted values
        actual (list): A list of actual values

    Returns:
        float | None: The score

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(predicted, list) or not isinstance(actual, list):
        return None
    if isinstance(predicted, list):
        for element in predicted:
            if not isinstance(element, float) and not isinstance(element, int):
                return None
    if isinstance(actual, list):
        for element in actual:
            if not isinstance(element, float) and not isinstance(element, int):
                return None
    if len(predicted) != len(actual):
        return None
    sum_mse = 0
    for i, elem in enumerate(predicted):
        sum_mse += (elem - actual[i]) ** 2
    return sum_mse / len(predicted)


def compare_profiles(
    unknown_profile: dict[str, str | dict[str, float]],
    profile_to_compare: dict[str, str | dict[str, float]],
) -> float | None:
    """
    Compare profiles and calculate the distance using symbols.

    Args:
        unknown_profile (dict[str, str | dict[str, float]]): A dictionary of an unknown profile
        profile_to_compare (dict[str, str | dict[str, float]]): A dictionary of a profile
            to compare the unknown profile to

    Returns:
        float | None: The distance between the profiles

    In case of corrupt input arguments or lack of keys 'name' and
    'freq' in arguments, None is returned
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    # проверка что ключи вообще есть
    required_keys = ['name', 'freq']
    for key in required_keys:
        if key not in unknown_profile or key not in profile_to_compare:
            return None
    # проверка что значение ключа name - строка
    if not isinstance(unknown_profile['name'], str):
        return None
    if not isinstance(profile_to_compare['name'], str):
        return None
    # проверка что значение ключа freq - число с плавающей точкой
    for key, value in unknown_profile['freq'].items():
        if not isinstance(key, str) or not isinstance(value, float):
            return None
    for key, value in profile_to_compare['freq'].items():
        if not isinstance(key, str) or not isinstance(value, float,):
            return None

    # вытаскиваем из словаря словарь с частотами
    frequency_unknown_profile = unknown_profile.get('freq')
    frequency_profile_to_compare = profile_to_compare.get('freq')

    tokens = set()
    for key in frequency_unknown_profile:
        tokens.add(key)
    for key in frequency_profile_to_compare:
        tokens.add(key)
    sorted_tokens = sorted(tokens)

    # создаем два списка со встречаемостью токенов
    new_list_unknown = []
    new_list_to_compare = []
    for element in sorted_tokens:
        if element in frequency_unknown_profile:
            new_list_unknown.append(frequency_unknown_profile.get(element))
        else:
            new_list_unknown.append(0)
        if element in frequency_profile_to_compare:
            new_list_to_compare.append(frequency_profile_to_compare.get(element))
        else:
            new_list_to_compare.append(0)

    some_mse = calculate_mse(new_list_unknown, new_list_to_compare)
    return some_mse


def detect_language(
    unknown_profile: dict[str, str | dict[str, float]],
    profile_1: dict[str, str | dict[str, float]],
    profile_2: dict[str, str | dict[str, float]],
) -> str | None:
    """
    Detect the language of an unknown profile.

    Args:
        unknown_profile (dict[str, str | dict[str, float]]): A dictionary of a profile
            to determine the language of
        profile_1 (dict[str, str | dict[str, float]]): A dictionary of a known profile
        profile_2 (dict[str, str | dict[str, float]]): A dictionary of a known profile

    Returns:
        str | None: A language

    In case of corrupt input arguments, None is returned
    """
    if not (
            isinstance(unknown_profile, dict) and
            isinstance(profile_1, dict) and
            isinstance(profile_2, dict)
    ):
        return None
    if not isinstance(unknown_profile['name'], str):
        return None
    if not isinstance(profile_1['name'], str):
        return None
    if not isinstance(profile_2['name'], str):
        return None
    # проверка что значение ключа freq - число с плавающей точкой
    for key, value in unknown_profile['freq'].items():
        if not isinstance(key, str) or not isinstance(value, float):
            return None
    for key, value in profile_1['freq'].items():
        if not isinstance(key, str) or not isinstance(value, float,):
            return None
    for key, value in profile_2['freq'].items():
        if not isinstance(key, str) or not isinstance(value, float,):
            return None

    mse_profile_1_and_unknown = compare_profiles(unknown_profile, profile_1)
    mse_profile_2_and_unknown = compare_profiles(unknown_profile, profile_2)

    if mse_profile_1_and_unknown < mse_profile_2_and_unknown:
        return profile_1['name']
    if mse_profile_2_and_unknown < mse_profile_1_and_unknown:
        return profile_2['name']


def load_profile(path_to_file: str) -> dict | None:
    """
    Load a language profile.

    Args:
        path_to_file (str): A path to the language profile

    Returns:
        dict | None: A dictionary with at least two keys – name, freq

    In case of corrupt input arguments, None is returned
    """


def preprocess_profile(profile: dict) -> dict[str, str | dict] | None:
    """
    Preprocess profile for a loaded language.

    Args:
        profile (dict): A loaded profile

    Returns:
        dict[str, str | dict] | None: A dict with a lower-cased loaded profile
            with relative frequencies without unnecessary n-grams

    In case of corrupt input arguments or lack of keys 'name', 'n_words' and
    'freq' in arguments, None is returned
    """


def collect_profiles(paths_to_profiles: list) -> list[dict[str, str | dict[str, float]]] | None:
    """
    Collect profiles for a given path.

    Args:
        paths_to_profiles (list): A list of strings to the profiles

    Returns:
        list[dict[str, str | dict[str, float]]] | None: A list of loaded profiles

    In case of corrupt input arguments, None is returned
    """


def detect_language_advanced(
    unknown_profile: dict[str, str | dict[str, float]], known_profiles: list
) -> list | None:
    """
    Detect the language of an unknown profile.

    Args:
        unknown_profile (dict[str, str | dict[str, float]]): A dictionary of a profile
            to determine the language of
        known_profiles (list): A list of known profiles

    Returns:
        list | None: A sorted list of tuples containing a language and a distance

    In case of corrupt input arguments, None is returned
    """


def print_report(detections: list[tuple[str, float]]) -> None:
    """
    Print report for detection of language.

    Args:
        detections (list[tuple[str, float]]): A list with distances for each available language

    In case of corrupt input arguments, None is returned
    """