import csv

def csv_opener(filename):
    #creates the dict from csv source
    pictionary = {}
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
                pictionary[row[0]] = [row[1], row[2]]
                #key - URL
                #0 - language
                #1 - topic

    return pictionary

def topic_mapper(website_content):
    newdoc = {}
    for url in website_content:
        topic = website_content[url][1]
        lang = website_content[url][0]
        if topic in newdoc:
            newdoc[topic].append(lang)
            newdoc[topic].append(url)
        else:
            newdoc[topic] = [lang, url]
    return newdoc

def paraleller(list):
    output = []
    for i in list:
        if list.index(i) % 2 == 1:
            x = """ <xhtml:link rel="alternate" hreflang=" """ + list[list.index(i)-1] + """ " href=" """ + i + """ " /> """
            output.append(x)
    return output

def csv_closer(filename2, dict):
    with open(filename2, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict.items():
            writer.writerow(value)


filename = input("path to input file (...../file.csv)?")
filename2 = input("path to export file (...../sitemap.xml)?")

website = csv_opener(filename)

topic_list = topic_mapper(website)

mapsite = open(filename2, 'a')

mapsite.write("\n" + """ <?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml"> """)

for specific_topic in topic_list:
    longitude = len(topic_list[specific_topic])
    if longitude > 2:
        xhtml_list = paraleller(topic_list[specific_topic])
        for item in topic_list[specific_topic]:
            if topic_list[specific_topic].index(item) % 2 == 1:
                mapsite.write("\n" + """ <url> """)
                mapsite.write("\n" + """ <loc> """ + item + """ </loc> """)
                for i in xhtml_list:
                    mapsite.write("\n" + i)
                mapsite.write("\n" + """ </url> """)
    else:
        mapsite.write("\n" + """ <url> """)
        mapsite.write("\n" + """ <loc> """ + topic_list[specific_topic][1] + """ <loc> """)
        mapsite.write("\n" + """ </url> """)

mapsite.close()
