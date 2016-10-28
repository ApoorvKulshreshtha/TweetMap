from flask import Flask, render_template,request,jsonify
from elasticsearch import Elasticsearch


application = Flask(__name__)
chab = ""

@application.route("/")
def index():
    elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
    result = elsr.search(size=5000,index='twitter')
    return render_template('tweet.html', result=parse(result))

@application.route('/ks', methods = ['GET','POST'])
def ks():
    key = request.form['search']
    elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
    updateKeywords(str(key))
    result = tweetmatch(elsr, str(key))
    return render_template('tweet.html', result=parse(result))

def tweetmatch(elsr, key):
    if len(key) is not 0:
      r = elsr.search(size=5000, index="twitter", body={"query": {"query_string": {"query": key}}})
    else:
      r = elsr.search(size=5000,index='twitter')
    return r

def updateKeywords(keyList):
  global chab
  chab = keyList

def parse(resul):
  for rl in resul['hits']['hits']:
    rl['_source']['text'] = ''.join(i for i in rl['_source']['text'] if ord(i)<128)
  return resul

@application.route('/rtw', methods = ['GET','POST'])
def rtw():
  elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
  global chab
  if len(chab) is not 0:
    result = elsr.search(size=5000, index="twitter", body={"query": {"query_string": {"query": chab}}})
  else:
    result = elsr.search(size=5000,index='twitter')

  return jsonify(parse(result))

  
if __name__ == "__main__":
	  application.run()