import json
import requests
from threading import Thread
import datetime


def get_new_id():
    x = json.loads(requests.post('https://www.menti.com/core/identifier', headers={"user-agent": ""}).text)
    return x["identifier"]


def get_info(pin, err=True):
    x = requests.get(
        'https://www.menti.com/core/vote-ids/' + str(pin) + "/series", headers={"user-agent": ""}).text
    try:
        return json.loads(x)
    except KeyError:
        if err:
            print("ERR: No such code")
            exit()
        return False


def print_info(info):
    i = 0
    activeid = info["pace"]["active"]
    print("Name:\t\t", info["name"])
    print("id:\t\t", info["id"])
    print("Pin:\t\t", info["vote_id"])
    print("last update:\t", datetime.datetime.strptime(
        (info["updated_at"]).replace("+00:00", ""), '%Y-%m-%dT%H:%M:%S'))
    print("No. questions:\t", len(info["questions"]))
    print("\nQuestion Specific:")
    for x in info["questions"]:
        i += 1
        if x["id"] == activeid:
            print("Question Nr:\t", i)
            print("Type:\t\t", x["type"])
            if (x["type"] == "wordcloud") | (x["type"] == "open"):
                print("Max Enteries:\t", x["max_nb_words"])

            elif (x["type"] == "choices") | (x["type"] == "choices_images") | (x["type"] == "winner") |\
                    (x["type"] == "ranking") | (x["type"] == "scales"):
                print("Choices:")
                for y in x["choices"]:
                    print("\tNo.:\t", y["position"] + 1)
                    print("\tlabel:\t", y["label"])
                    print("\tid:\t", y["id"], "\n")
            print("Question name:\t", x["question"])
            print("Public Key:\t", x["public_key"])


def list_info(info):
    l = []
    i = 0
    activeid = info["pace"]["active"]
    l.append("Name: " + info["name"])
    l.append("id: " + info["id"])
    l.append("Pin: " + str(info["vote_id"]))
    l.append("last update: " + str(datetime.datetime.strptime(
        (info["updated_at"]).replace("+00:00", ""), '%Y-%m-%dT%H:%M:%S')))
    l.append("No. questions: " + str(len(info["questions"])))
    l.append("Question Specific:")
    for x in info["questions"]:
        i += 1
        if x["id"] == activeid:
            l.append("Question Nr: " + str(i))
            l.append("Type: " + x["type"])
            if (x["type"] == "wordcloud") | (x["type"] == "open"):
                l.append("Max Enteries: " + str(x["max_nb_words"]))

            elif (x["type"] == "choices") | (x["type"] == "choices_images") | (x["type"] == "winner") |\
                    (x["type"] == "ranking") | (x["type"] == "scales"):
                l.append("Choices:")
                for y in x["choices"]:
                    l.append("  No.: " + str(y["position"] + 1))
                    l.append("  label: " + y["label"])
                    l.append("  id: " + str(y["id"]) + "\n")
            l.append("  Question name: " + str(x["question"]))
            l.append("  Public Key: " + str(x["public_key"]))
    return l


def get_active_id(info):
    return info["pace"]["active"]


def get_active_questionid(info):
    activeid = info["pace"]["active"]
    for x in info["questions"]:
        if x["id"] == activeid:
            return x["public_key"]


def get_active_question_type(info):
    activeid = info["pace"]["active"]
    for x in info["questions"]:
        if x["id"] == activeid:
            return x["type"]


def get_active_question(info):
    activeid = info["pace"]["active"]
    for x in info["questions"]:
        if x["id"] == activeid:
            return x["choices"]


def get_active_question_min_max(info):
    activeid = info["pace"]["active"]
    for x in info["questions"]:
        if x["id"] == activeid:
            return x["range"]


def answer(question_id, type, id, info, answer_p):

    headers = {
        "x-identifier": id,
        "cookie": "identifier1=" + id,
        "Content-Type": "application/json",
    }
    if type == "qfa":
        quesid = info["id"]

        series = json.loads(requests.get(
            url='https://www.menti.com/core/vote-keys/' + quesid + '/qfa', headers={"user-agent": ""}).text)

        series = series["series_id"]

        data = {"series_id": series, "question": answer_p, "user-agent": ""}

        requests.post(url='https://www.menti.com/core/qfa',
                      data=json.dumps(data), headers=headers)

    else:

        t = get_active_question_type(info)
        u = get_active_question(info)
        if (t == "choices") | (t == "choices_images") | (t == "winner") | (t == "ranking"):
            # cross reference
            for x in u:
                if x["position"] + 1 == answer_p:
                    awnser = [(x["id"])]

        data = {"question_type": type, "vote": answer_p}
        # print(data)

        headers = {
            "x-identifier": id,
            "cookie": "identifier1=" + id,
            "Content-Type": "application/json",
            "user-agent": ""
        }

        requests.post(url='https://www.menti.com/core/votes/' +
                      question_id, data=json.dumps(data), headers=headers)


def spam(word):
    ids = []
    idtred = []

    def add_new_id_to_list():
        global ids
        ids.append(get_new_id())

    for x in range(1):
        t1 = Thread(target=add_new_id_to_list)
        idtred.append(t1)
