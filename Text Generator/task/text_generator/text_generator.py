import random
from collections import defaultdict


def get_trigrams(words):
    bigrams = []
    for i in range(len(words) - 2):
        bigrams.append((f'{words[i]} {words[i + 1]}', words[i + 2]))
    return bigrams


def get_heads_to_tails_counts(trigrams):
    heads_to_tails = defaultdict(lambda: defaultdict(int))
    for head, tail in trigrams:
        heads_to_tails[head][tail] += 1
    return heads_to_tails


def get_next_word(heads_to_tails, two_last_words):
    tails = heads_to_tails[two_last_words]
    next_word = random.choices(
        list(tails.keys()),
        weights=list(tails.values())
    )[0]
    return next_word


def get_first_two_words(heads_to_tails):
    return random.choice(list(heads_to_tails.keys()))


def get_sentence(heads_to_tails):
    is_sentence_finished = False
    current_word = get_first_two_words(heads_to_tails)
    sentence_words = []

    while not is_sentence_finished:
        words_count = len(sentence_words)
        is_valid_last_word = current_word[-1] in ".!?"
        first_current_word = current_word.split()[0]
        is_valid_first_word = (first_current_word[0].isupper()
                               and first_current_word[-1] not in ".!?")

        if words_count == 0:
            if is_valid_first_word:
                sentence_words.extend(current_word.split())
                current_word = get_next_word(
                    heads_to_tails,
                    " ".join(sentence_words[-2:])
                )
            else:
                current_word = get_first_two_words(heads_to_tails)
        elif words_count >= 4:
            sentence_words.append(current_word)

            if is_valid_last_word:
                is_sentence_finished = True
            else:
                current_word = get_next_word(
                    heads_to_tails,
                    " ".join(sentence_words[-2:])
                )
        else:
            sentence_words.append(current_word)
            current_word = get_next_word(
                heads_to_tails,
                " ".join(sentence_words[-2:])
            )

    return " ".join(sentence_words)


def main():
    file = open(input(), "r", encoding="utf-8")
    text = file.read()
    words = text.split()
    bigrams = get_trigrams(words)
    heads_to_tails = get_heads_to_tails_counts(bigrams)

    for _ in range(10):
        print(get_sentence(heads_to_tails))

    file.close()


if __name__ == "__main__":
    main()
