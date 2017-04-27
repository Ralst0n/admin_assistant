import yaml
import requests
from bs4 import BeautifulSoup
import webbrowser
import time


#uid_0 > div._OKe > div:nth-child(2) > div.kp-header > div > div._cFb > div > div > div._XWk
def bootup():
    with open("config.yml", 'r') as c:
        config = yaml.load(c)

    with open("chatbot.yml", 'r') as chat:
        chatyml = yaml.load(chat)

    while True:
        print("[{}]: What can I answer for you, {}?".format(chatyml["name"], config["user"]))
        question = input("[{}]: ".format(config["user"]))
        if question == "" or question.lower() == "bye":
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


    return "idk"

def goog_it(question):
    query = question.split()
    return ("https://www.bing.com/search?q=" + "+".join(query))

if __name__ == "__main__":
    bootup()
