import yaml
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from random import randint


#uid_0 > div._OKe > div:nth-child(2) > div.kp-header > div > div._cFb > div > div > div._XWk
def bootup():
    with open("config.yml", 'r') as c:
        config = yaml.load(c)

    with open("chatbot.yml", 'r') as chat:
        chatyml = yaml.load(chat)

    while True:
        print("[{}]: What can I do for you, {}?".format(chatyml["name"], config["user"]))
        question = input("[{}]: ".format(config["user"]))
        if question == "" or question.lower() == "bye" or question.lower() == "im leaving":
            print("[{}]: Okay, I'll send you back to the main menu.".format(chatyml["name"]))
            print("[{}]: See you next time, {}!".format(chatyml["name"], config["user"]))
            time.sleep(2)
            break
        answer = check_google(question)
        if answer == "idk":
            print("[{}]: I..".format(chatyml["name"], check_google(question)))
            time.sleep(1)
            print("[{}]: I don't know :(".format(chatyml["name"]))
            time.sleep(1)
            go_google = input("[{}]: Do you want to ask a smarter bot? \n[{}]: ".format(chatyml["name"], config["user"]))
            if go_google:
                webbrowser.open(goog_it(question))
        else:
            print("[{}]: {}".format(chatyml["name"], check_google(question)))
        # take_input= input("[{}]: ".format(config["user"]))
        time.sleep(2)

def check_google(question):
    answer = ""
    search = goog_it(question)
    results = requests.get(search)
    soup = BeautifulSoup(results.content, "lxml")
    for ele in soup.find_all('div', class_ = "b_focusTextMedium"):
        answer = ele.text
        return answer
    for ele in soup.find_all('div', class_ = "b_focusTextLarge"):
        answer = ele.text
        return answer
    for ele in soup.find_all('div', class_ = "b_focusTextSmall"):
        answer = ele.text
        return answer
    for ele in soup.find_all('div', class_ = "rwrl"):
        if len(ele.text.split("is")[0]) > len(ele.text.split("average")[0]):
            long_answer = ele.text.split("average ")[-1]
        else:
            long_answer = ele.text.split("is ")[-1]

        if len(long_answer.split('.')[0]) > 230:
            return long_answer.split('.')[0][:230]
        else:
            return long_answer.split('.')[0]
    for ele in soup.find_all('h2', class_="b_entityTitle"):
        answer = ele.text
        return "maybe the {}".format(answer)

    return "idk"

def goog_it(question):
    query = question.split()
    return ("https://www.bing.com/search?q=" + "+".join(query))

def future(array):
    '''checks if the question contains future words, if it does, gives a random answer'''
    response_words = []
    #if its a should with an or clause pick one of the sides of the or
    if (array[0].lower() == "should" or array[0].lower() == "will") and "or" in array:
        or_index = array.index("or")
        # if array[1].lower() in ["i", "we"] or "and i" or in array or "and me" in array:
        #     for word in ["You", array[0].lower()]:
        #         response_words.append(word)
        # elif array[1].lower() == "you":
        #     for word in "You #{}".format(array[0].lower()).split():
        #         response_words.append(word)
        # else:
        #     response_words.append(array[1])
        #     response_words.append(array[0].lower())
        i = randint(0,1)
        if i == 1:
            choice = " ".join(array[2:])
        else:
            choice = " ".join(array[or_index + 1:])
    else:
        choices = ["Yes", "No", "Maybe", "Probably", "Probably not", "No Chance", "Of Course"]
        idx = randint(0, len(choices)-1)
        choice = choices[idx]
    return choice

class Question:
    def __init__(self):
        pass


class ChatBot:
    def __init__(self, config, chatbot):
        self.config = config
        self.chatbot = chatbot
        print("[{}]: Hello {}. How are you today?".format(chatbot, config))

    def interpret(self, question):
        q_parts = question.split(" ")



if __name__ == "__main__":
    bootup()
