import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import html  
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
def AmzonParser(url2, asin):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page2 = requests.get(url2,headers=headers)


    while True:
        #sleep(3)
        try:
            doc2 = html.fromstring(page2.content) 

            XPATH_DESCRIPTION = '//*[@id="productDescription"]/p/text()'
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            stop_words = set(stopwords.words('english'))





            RAW_NAME = doc2.xpath(XPATH_NAME)
            RAW_DESCRIPTION = doc2.xpath(XPATH_DESCRIPTION)
            RAW_CATEGORY = doc2.xpath(XPATH_CATEGORY)
     

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            DESCRIPTION = ' '.join(''.join(RAW_DESCRIPTION).split()[:30]).strip() if RAW_DESCRIPTION else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None

            word_tokens = word_tokenize(DESCRIPTION)

 
            filtered_sentence = ""
 
            for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence = filtered_sentence + w + " "

           
            if page2.status_code!=200:
                raise ValueError('captha')
                return None
            data = CATEGORY + "," + filtered_sentence + "," + NAME
 
            return data
        except Exception as e:
            print "Exception"
            print e
            return None
 
def ReadAsin(i):

   
    url2 = "https://www.amazon.com/dp/"+i
    print "Processing: "+url2
    data = AmzonParser(url2, i)
    if(data != None):
        return data
    else:
        return None 
 
if __name__ == "__main__":
    ReadAsin('B06XCM2731')
