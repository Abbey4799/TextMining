import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(text):
    wc=WordCloud(background_color='white',font_path="C:\\Windows\\Fonts\\STSONG.TTF",max_words=150,width=1000,height=860,stopwords=STOPWORD).generate(text)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

good=""
bad=""
STOPWORD=['论文','给分','考试','内容','期末考试']

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.local
collection = db['manual_tagging']
for item in collection.find():
    if int(item['Tendency'])==1:
        good+=str(item['comment_wihout_stpw'])
    else:
        bad+=str(item['comment_wihout_stpw'])

generate_wordcloud(bad)
