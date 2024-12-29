import json


def set_max_score(new_score):
    dic = {"score": new_score}

    with open("assets/data.json", "w") as outfile:
        json.dump(dic, outfile)


def get_max_score():
    with open("assets/data.json", "r") as infile:
        data = json.load(infile)

        return data["score"]
