import urllib.request as urllib2
from bs4 import BeautifulSoup
import wikipedia
from deep_translator import GoogleTranslator

# get languages
soup = BeautifulSoup(urllib2.urlopen('http://en.wikipedia.org/wiki/Citation'))
links = [(el.get('lang'), el.get('title')) for el in soup.select('li.interlanguage-link > a')]

for language, title in links:
    page_title = title.split(u' – ')[0]
    wikipedia.set_lang(language)
    page = wikipedia.page(page_title)
    print(language)
    words1 = (page.summary)
    #print(words1)
    sentence_index = words1.find('.')
    sentence_index += 1
    words3 = (words1[0: sentence_index])
    #print(words3)
    try:
      translated = GoogleTranslator(source='auto', target='en').translate(words3) 
    except:
      pass
    print(translated)
    print("-----")
