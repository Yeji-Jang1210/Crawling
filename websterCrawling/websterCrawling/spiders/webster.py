import scrapy
import csv
from urllib import parse

#some wrong words
match_words = [('tv','television')]

#read csv file
def ConvertCSVfileToList():
    elements = []
    csvFile = 'dictionary.csv'
    with open(csvFile) as read_object:
        csv_reader = csv.reader(read_object)
        list_of_csv = list(csv_reader)
    for element in list_of_csv:
        elements += element
    elements_set = set(elements)
    seed_list = list(elements_set)
    seed_list.remove('')
    return seed_list

def parse_content(response, str_xpath):
    return ' '.join(response.xpath(str_xpath).extract())

class WebsterSpider(scrapy.Spider):

    words = ConvertCSVfileToList()
    print(words)

    for (wrong, correct) in match_words:
        words[words.index(wrong)] = correct

    name = 'webster'
    allowed_domains = ['https://www.merriam-webster.com/dictionary']
    start_urls = ['https://www.merriam-webster.com/dictionary/' + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        item = []
        entryPath = response.xpath('string(//*[@id="dictionary-entry-1"]/div[1]/div/p)').extract()
        num = 1
        if entryPath is None:
            num = int(' '.join(entryPath)[-2])
        if num is str:
            num = 1

        for i in range(1, num+1):
            path = '//*[@id="dictionary-entry-' + str(i) +'"]/div[contains(@class,"vg")]'
            for sb in response.xpath(path):
                for sbNum in sb.xpath('./div[contains(@class,"sb")]'):
                    for sbStr in sbNum.xpath('./span'):
                        item.append(parse_content(sbStr,'string(./div/span[contains(@class,"dt")]/span)')+"\n")
                        path = './div[contains(@class,"pseq")]/div[contains(@class,"sense")]'
                        if sbStr.xpath(path) is None:
                            path = './div[contains(@class,"sense")]'
                        for sense in sbStr.xpath(path):
                            item.append(parse_content(sense,'string(./span[contains(@class,"dt")]/span[contains(@class,"dtText")])')+"\n")

        for examples in response.xpath('//*[@id="examples-anchor"]/div[contains(@class,"in-sentences")]'):
            for sentence in examples.xpath('./span[contains(@class,"ex-sent")]'):
                item.append(parse_content(sentence,'string()').lstrip().replace("‘","").replace("’","") + "\n")

        for recentExamples in response.xpath('//*[@id="examples-anchor"]/div[contains(@class,"on-web")]'):
            for sentence in recentExamples.xpath('./span[contains(@class,"ex-sent")]/span[contains(@class,"t")]'):
                item.append(parse_content(sentence,'string()').lstrip().replace("‘","").replace("’","") + "\n")

        with open('./data/' + parse.unquote(word).replace(" ","") +'.txt','w',encoding='UTF-8') as f:
            for element in item:
                f.write(str(element))

        pass
