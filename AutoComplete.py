#import AutoCompleteData
import os
import operator


class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, completed_sentence, offset, score, source_text):
        self.completed_sentence = completed_sentence
        self.score = score
        self.source_text = source_text
        self.offset = offset


d = dict()
path = "C:\\Users\\avita\\Desktop\\Bootcamp\\google\\2021-archive"


def init():
    offset = 0
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".txt"):
                f = open(filepath, "r")
                lines = f.readlines()
                for line in lines:
                    offset += 1
                    for word in line.split(" "):
                        word = word.lower()
                        if word in d:
                            d[word] += [(offset, filepath, line)]
                        else:
                            d[word] = [(offset, filepath, line)]



def if_can_change_one_char(prefix, check):
    counter = 0
    change_index = 0
    if len(check)!=len(prefix):
        return 0, False
    for index in range(len(prefix)):
        if prefix[index] != check[index]:
            counter += 1
            change_index = index
    if counter == 1:
        if change_index == 0:
            return 5, True
        elif change_index == 1:
            return 4, True
        elif change_index == 2:
            return 3, True
        elif change_index == 3:
            return 2, True
        elif change_index >= 4:
            return 1, True
    else:
        return 0, False


def if_can_add_one_char(pre, to_check):
    # pre- static
    # check- change
    rng = range(len(to_check))
    for i in rng:
        change = to_check[:i] + to_check[i + 1:]
        if change == pre:
            if i == 0:
                return 10, True
            elif i == 1:
                return 8, True
            elif i == 2:
                return 6, True
            elif i == 3:
                return 4, True
            elif i >= 4:
                return 2, True
    else:
        return 0, False


def first_word(first_prefix):
    return list(filter(lambda x: same_or_try_fix(first_prefix, x)[1], d.keys()))


def if_can_remove_one_char(prefix, check):
    # pre- static
    # check- change
    counter = 0
    change_index = 0
    j = 0
    for i in range(len(prefix)):
        if j < len(check):
            if prefix[i] != check[j]:
                counter += 1
                j -= 1
                change_index = i
            j += 1
    if counter == 1:
        if change_index == 0:
            return 10, True
        elif change_index == 1:
            return 8, True
        elif change_index == 2:
            return 6, True
        elif change_index == 3:
            return 4, True
        elif change_index >= 4:
            return 2, True
    else:
        return 0, False


def same_or_try_fix(pre, check):
    if abs(len(pre) - len(check)) >= 2:
        return 0, False, False
    score1, can_change = if_can_change_one_char(pre, check)
    score2, can_add = if_can_add_one_char(pre, check)
    score3, can_remove = if_can_remove_one_char(pre, check)
    # 0-score 1-match 2 -fix
    if pre == check:
        return 0,True, False
    elif can_change:
        return score1, True, True
    elif can_add:
        return score2, True, True
    elif can_remove:
        return score3, True, True
    return 0, False, False


def get_best_k_completions(prefix: str):# -> list[AutoCompleteData]
    prefix = prefix.lower()
    all_matches = []
    pre_vec = prefix.replace(',', '').split(" ")

    for op_word in first_word(pre_vec[0]):
        score = len(prefix)*2
        for detail in d[op_word]:
            only_one_change = True
            i = detail[2].lower().index(op_word)
            to_check = detail[2][i:]
            to_check = to_check.lower().strip().split(' ')
            match = False
            if len(to_check) < len(pre_vec):
                break
            else:
                for i in range(len(pre_vec)):  # pass on each word in the prefix
                    if detail[2] != '' and i < len(to_check):
                        add_to_score, match, can_fix = same_or_try_fix(pre_vec[i], to_check[i])
                        if can_fix and only_one_change:
                            only_one_change = False
                            score -= add_to_score
                        elif not match or (can_fix and not only_one_change):
                            match = False
                            break  # no match to this sentence
            if match:
                a = AutoCompleteData(detail[2], detail[0], score, detail[1])
                all_matches.append(a)
    all_matches = sorted(all_matches, key=lambda x: (x.score, x.completed_sentence) , reverse=True)
    return all_matches


def print_top_5(all_matches):
    counter = 1
    if all_matches:
        for auto_comp in all_matches:
            if counter > 5:
                return
            print(str(counter) + ". " + auto_comp.completed_sentence.strip() + " (" + auto_comp.source_text + " " + str(auto_comp.offset) + ")" + str(auto_comp.score))
            counter += 1


def main():

    print("Loading the files and preparing the system...")
    init()
    print("the system is ready. Enter your text:")
    while True:
        flag = True
        the_input = input()
        while flag:
            top_5 = get_best_k_completions(the_input)
            print_top_5(top_5)
            print(the_input, end="")
            inp = input()
            if inp == "#":
                flag = False
            else:
                the_input += inp
        print("A new search begins:")


if __name__ == "__main__":
    main()