from snownlp import SnowNLP
import pymongo

def snownlp_score():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    comment_collection = db['manual_tagging']
    
    for item in comment_collection.find():
        item['snownlp_score']=SnowNLP(item['comment']).sentiments
        comment_collection.save(item)
    
snownlp_score()
