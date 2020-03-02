import sys  # argvs
from bs4 import BeautifulSoup  # parsing html
import requests  # get site html
import re  # regex
import subprocess


def get_args():
    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])
    return args


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.readlines()


def save_to_file(file_path, lines):
    with open(file_path, "r+") as file:
        file.writelines(lines)


def get_file_path(args):
    args2 = []
    for arg in args:
        arg = re.findall(".+.txt", arg)
        if len(arg) is not 0:
            args2.append(arg)
    if len(args2) > 1 or len(args2) == 0:
        return None
    else:
        return args2[0][0]


def get_country_codes(args):
    args2 = []
    for arg in args:
        args2.append(re.findall("\.[a-zA-Z]{2,3}", arg))
    args3 = [x for x in args2 if x]  # get rid of empty elements
    args2.clear()
    args2 = [word[1:] for arg in args3 for word in arg if word != ".txt"]
    if len(args2) == 0:
        return None
    return args2


def get_options(args):
    args2 = []
    for arg in args:
        args2.append(re.findall("-.{1,}", arg))
    args3 = [letter for arg in args2 for word in arg for letter in word if letter != '-']
    return args3


def specify_option(item, options):
    item.replace("\n", "")  # get rid of newlines
    print("More than one match found for " + item)
    number = 1
    for t in options:
        print(str(number) + ". " + t, sep='')
        number += 1
    user_input = input("Please specify one: ")
    if int(user_input):
        return int(user_input) - 1
    else:
        print(user_input + " is not a number")
        return specify_option(item, options)


def get_from_wikipedia(country_code, item):
    site = "https://" + country_code + ".wikipedia.org/w/index.php?search=" + item
    description = []
    try:
        source = requests.get(site).text
        soup = BeautifulSoup(source, 'lxml')
        # no results
        if soup.find('div', class_="mw-search-form-wrapper"):
            description.append("")
            site = ""
        else:
            article = soup.find('div', class_="mw-parser-output")
            p_list = article.find_all('p', recursive=False)
            # one result
            if len(p_list) > 1:
                for p in p_list:
                    string = p.text
                    if string != "" and string != "\n":
                        string = re.sub("\[[0-9]*]", "", string)  # get rid of [1],[2] etc
                        string = re.sub("\\xa0", " ", string)  # get rid of \xa0
                        description.append(string)
            # more than one result
            else:
                titles = []
                descriptions = []
                for li in article.find_all('li'):
                    part = li.find('a', href=True)
                    titles.append(part['title'])
                    descriptions.append(li.text)
                selected_item = titles[specify_option(item, descriptions)]
                return get_from_wikipedia(country_code, selected_item)
    except ConnectionError:
        print("Connection error at " + item)
        description.append("")
        site = ""
    return description, site


def refactor_string(item):
    item.replace("\n", "")  # get rid of newlines
    item.replace(" ", "")  # get rid of spaces
    item = re.sub("\ +", "_", item)  # replace spaces with '_' (for www address)
    return item


def process_country_codes(country_codes, code_index, item):
    if country_codes is None:
        country_codes = ["en"]
    if len(country_codes) - 1 < code_index:
        return "", ""
    description, item_url = get_from_wikipedia(country_codes[code_index], item)
    if item_url == "":
        return process_country_codes(country_codes, code_index + 1, item)
    return description, item_url


def start(args):
    not_found = 0
    file_path = get_file_path(args)
    if file_path is None:
        print("Please specify txt file path. ex: WikiSearch myTextFile.txt")
    else:
        options = get_options(args)
        country_codes = get_country_codes(args)
        to_write = []
        for line in read_file(file_path):
            if line is not "" or " ":
                description, item_url = process_country_codes(country_codes, 0, refactor_string(line))
                if item_url == "":
                    not_found += 1
                if 'v' in options:
                    print(line + ": not found" if item_url is "" else line + ": " + description[0])
                if 'e' in options:
                    string = ''.join(description)
                    to_write.append(line + string + item_url)
                else:
                    to_write.append(line + description[0] + item_url)
        save_to_file(file_path, to_write)
        print(
            "Results saved to " + file_path if not_found is 0 else "Results saved to " + file_path + ". Not found " + str(
                not_found) + " items")
        if "o" in options:
            subprocess.call(["nano", file_path])


if __name__ == "__main__":
    start(get_args())
