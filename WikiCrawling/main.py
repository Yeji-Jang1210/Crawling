import wikipediaapi
import pandas
import csv

def FindWikipediaPage(words):
    isExists = False
    for i in range(len(words)):
        page_py = wiki_wiki.page(words[0:i + 1] + " " + words[i + 1:])
        if page_py.exists():
            isExists = True
            break
    if isExists:
        return True
    else:
        return False
def ConvertCSVfileToList():
    elements = []
    with open('dictionary.csv') as read_object:
        csv_reader = csv.reader(read_object)
        list_of_csv = list(csv_reader)
    for element in list_of_csv:
        elements += element
    ####중복제거####
    # 집합 set으로 변환
    elements_set = set(elements)
    # list으로 변환
    seed_list = list(elements_set)
    seed_list.remove('')
    print(seed_list)
    return seed_list


def IsPageExists(word):
    page_py = wiki_wiki.page(word)
    if page_py.exists():
        return True
    else:
        if FindWikipediaPage(word):
            return True
        else:
            return False

wiki_wiki = wikipediaapi.Wikipedia('en')
objects = ['dining room']
for word in objects:
    item = []
    if IsPageExists(word):
        page_py = wiki_wiki.page(word)
        item.append(page_py.title)
        item.append(page_py.text)
        with open('./wiki_data/' + 'dining_room_wiki'+'.txt','w',encoding='UTF-8') as f:
            for element in item:
                f.write(str(element))
        print(word + "succeeded")
    else:
        print("not found")
