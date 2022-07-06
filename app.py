from asyncore import read
from flask import Flask,request
from pymongo import MongoClient
import datetime
from flask_cors import CORS
from bson.objectid import ObjectId

    

app=Flask(__name__)
CORS(app)

connection="mongodb+srv://nahid:khan2019@project.ncsynjh.mongodb.net"
#connection="mongodb://localhost:27017"

client=MongoClient(connection)

db=client.themuslimcoder

collection=db.articles
#collection=db.articlesaboutcoding

def get_date():
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    e = datetime.datetime.now()
    
    
    return f"{months[e.month]} {e.day}, {e.year}"




@app.route('/get/<aid>')
def get_post(aid):
    objid = ObjectId(aid)
    article=collection.find_one({'_id':objid})
    article.pop('_id')
    article['id']=aid
    read_more=collection.find({"tag":"recent"})
    more_article_list=[
        {
            "id":str(x['_id']),
            "title":x['title'],
            "banner":x['banner'],
            "language":x['language'],
            "date":x['date'],
            "read_time":x['read_time']
        }
     for x in read_more]

    #print(more_article_list)
    #return {"requested_article":[article, more_article_list]}
    article['more_section']=more_article_list
    return article

@app.route('/create_subscriber',methods=['POST'])
def createSubscriber():
    try:
        email = request.get_json()
        subscribers=db.subscribers
        subscribers.insert_one(email)
        return {"response":True}
    except:
        return {"response":False}


@app.route('/get_all')
def get_all():
    articles=collection.find({"tag":"recent"})
    docs=[]
    for i in articles:
        ids=i['_id']
        i.pop('_id')
        i['id']=str(ids)
        docs.append(i)
    return {"recent_articles":docs}


if __name__ =="__main__":
    app.run(debug=True)
