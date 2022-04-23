import json


def similarity(word1, word2):
    """Compares two words and returns a integer that represents much overlap there is between the two words' letters,
     weighting highly """
    counter = 0
    used = []
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            counter += 8
        elif word1[i] in word2 and word1[i] not in used:
            counter += 4
        if word1[i] in used:
            counter += -1
        used.append(word1[i])
    return counter


def make_dictionary(word_list):
    """Takes in a list of words and creates a dictionary where the keys are the words from the list and the
    values are the sum of the similarities of those words with all other words in the list."""
    word_dict = {}
    for word in word_list:
        count = 0
        for i in range(len(word_list)):
            count += similarity(word, word_list[i])
        word_dict[word] = count
    return word_dict


def best_word(word_dict):
    """Takes in a dictionary of words and their overlap sum and returns a tuple containing
    the key with the highest sum and the sum."""
    keys = list(word_dict.keys())
    max_word = keys[0]
    max_value = word_dict[keys[0]]
    for key in keys:
        if word_dict[key] > max_value:
            max_word = key
            max_value = word_dict[key]
    return max_word, max_value


def check_removal(list_word, word, results):
    """Takes in two words and a list representing the inclusion or exclusion of letters in the second word and returns
    True if the inclusions and exclusions in the second word disqualify the first word. Returns False otherwise."""
    letters = {}
    danger = []
    for j in range(len(word)):
        if results[j] == 2:
            if word[j] != list_word[j]:
                return True
            else:
                try:
                    letters[word[j]] += 1
                except KeyError:
                    letters[word[j]] = 1
        if results[j] == 1:
            if word[j] == list_word[j]:
                return True
            else:
                try:
                    letters[word[j]] += 1
                except KeyError:
                    letters[word[j]] = 1
        if results[j] == 0:
            if word[j] == list_word[j]:
                return True
            else:
                try:
                    letters[word[j]] += 0
                except KeyError:
                    letters[word[j]] = 0
                danger.append(word[j])
    for key in list(letters.keys()):
        if list_word.count(key) < letters[key] or (list_word.count(key) != letters[key] and key in danger):
            return True
    return False


def reduce(words_list, word, results):
    """Takes in a list of words, a word, and a list representing the inclusion or exclusion of words in that list
    and returns a new list made up of those words that the combination of the given word and results allow to remain."""
    new_list = []
    for i in range(len(words_list)):
        if check_removal(words_list[i], word, results) is False:
            new_list.append(words_list[i])
    return new_list


def get_best_word(words, conditions):
    """Takes in a list of characters and an array of arrays of conditions and returns the best word to solve the
    Wordle based on the reduced list created by the removal of words based on the words and conditions."""
    js = open("words.json", "r")
    all_words = json.load(js)
    js.close()
    i = 0
    while i < 6 and words[i][4] != '':
        word = ""
        word = word.join(words[i]).lower()
        all_words = reduce(all_words, word, conditions[i])
        i += 1
    if i == 0:
        return "stare"
    dictionary = make_dictionary(all_words)
    return best_word(dictionary)[0]


def word_response(word, solution_inx, sol_list="words.json"):
    scrabble = open("scrabble.json", "r")
    all_words = json.load(scrabble)
    sols = open(sol_list, "r")
    solutions = json.load(sols)
    sols.close()
    scrabble.close()
    solution = solutions[solution_inx % len(solutions)]
    if word not in all_words:
        return False
    else:
        conditions = [0 for i in range(len(word))]
        for i in range(len(word)):
            if word[i] == solution[i]:
                conditions[i] = 2
                solution = solution[:i] + "0" + solution[i+1:]
                word = word[:i] + "1" + word[i+1:]
        for i in range(len(word)):
            if solution.count(word[i]) > 0:
                conditions[i] = 1
                solution = solution.replace(word[i], "0", 1)
        return conditions
