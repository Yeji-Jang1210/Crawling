import scrapy
import csv
import wikipediaapi

match_words = [('diningroom','dining_room'),('livingroom','living_room'),('sidetable','side_table')]


def ConvertCSVfileToList():
    elements = []
    with open('dictionary.csv') as read_object:
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


class ScrapyOxfordSpider(scrapy.Spider):

    words = ConvertCSVfileToList()

    for (wrong, correct) in match_words:
        words[words.index(wrong)] = correct

    name = 'scrapy_oxford'
    allowed_domains = ['www.lexico.com/en/definition']
    start_urls = ['https://www.lexico.com/en/definition/' + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        item = []
        item.append(response.xpath('//span[contains(@class,"hw")]/text()').extract()[0] + "\n")
        for section in response.xpath('//*[@id="content"]/div[1]/div[2]/div/div/div/div/section'):
            for trg in section.xpath('./ul/li'):
                item.append(parse_content(trg,'./div/p/span[contains(@class,"ind")]/text()')+"\n")

                item.append(parse_content(trg,'./div/div[contains(@class,"exg")]/div/em/span/text()').replace("‘","").replace("’","") + "\n")

                for list in trg.xpath('./div/div[contains(@class,"examples")]/div[contains(@class,"exg")]/ul/li'):
                    item.append(parse_content(list,'./em/text()').replace("‘","").replace("’","") + "\n")
                    print(list.xpath('./em/text()').extract())
                #ol subSenses
                for subSenses in trg.xpath('./div/ol/li'):
                    item.append(parse_content(subSenses,'./span[contains(@class,"ind")]/text()') + "\n")

                    sub_discription = parse_content(subSenses,'./div[2]/div/em/span[contains(@class," one-click-content")]/text()')
                    item.append(sub_discription.replace("‘","").replace("’","").lstrip()+"\n")

                    for subSenses_example_sentence in subSenses.xpath('./div[3]/div[2]/ul/li'):
                        item.append(parse_content(subSenses_example_sentence,'./em/text()').replace("‘","").replace("’","") + '\n')

        with open('./data/' + word +'.txt','w',encoding='UTF-8') as f:
            for element in item:
                f.write(str(element))
        pass
