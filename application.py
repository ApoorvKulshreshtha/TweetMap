from flask import Flask, render_template,request,jsonify
from elasticsearch import Elasticsearch


application = Flask(__name__)
chab = ""

@application.route("/")
def home():
    es = Elasticsearch([{'host':'search-tweet-c3mkhiza33cstn5qrvotrsw7my.us-west-2.es.amazonaws.com', 'port':443,'use_ssl':True}])
    result = es.search(size=5000,index='twitter')
    return render_template('tweet.html', result=parseRes(result))

@application.route('/keysearch', methods = ['GET','POST'])
def keysearch():
    keywords = request.form['search']
    es = Elasticsearch([{'host':'search-tweet-c3mkhiza33cstn5qrvotrsw7my.us-west-2.es.amazonaws.com', 'port':443,'use_ssl':True}])
    updateKeywords(str(keywords))
    result = tweetmatch(es, str(keywords))
    return render_template('tweet.html', result=parseRes(result))

def tweetmatch(es, keyword):
    if len(keyword) is not 0:
      res = es.search(size=5000, index="twitter", body={"query": {"query_string": {"query": keyword}}})
    else:
      res = es.search(size=5000,index='twitter')
    return res

def updateKeywords(keywordList):
  global chab
  chab = keywordList

def parseRes(result):
  for r in result['hits']['hits']:
    r['_source']['text'] = ''.join(i for i in r['_source']['text'] if ord(i)<128)
  return result

@application.route('/rt', methods = ['GET','POST'])
def rt():
  es = Elasticsearch([{'host':'search-tweet-c3mkhiza33cstn5qrvotrsw7my.us-west-2.es.amazonaws.com', 'port':443,'use_ssl':True}])
  global chab
  if len(chab) is not 0:
    result = es.search(size=5000, index="twitter", body={"query": {"query_string": {"query": chab}}})
  else:
    result = es.search(size=5000,index='twitter')
  print('server loop')
  print(len(result['hits']['hits']))
  print('exit server loop')
  return jsonify(parseRes(result))

  
if __name__ == "__main__":
	  application.run()