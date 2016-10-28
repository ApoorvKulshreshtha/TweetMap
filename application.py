from flask import Flask, render_template,request,jsonify
from elasticsearch import Elasticsearch


application = Flask(__name__)
chab = ""

def tweetmatch(elsr, key):
  if len(key) is 0:
    r = elsr.search(size=5000,index='twitter')
  else:
    r = elsr.search(size=5000, index="twitter", body={"query": {"query_string": {"query": key}}})
  return r

def updateKeyList(keyList):
  global chab
  chab = keyList

def parse(resul):
  for rl in resul['hits']['hits']:
    rl['_source']['text'] = ''.join(i for i in rl['_source']['text'] if ord(i)<128)
  return resul

@application.route('/ks', methods = ['GET','POST'])
def ks():
    key = str(request.form['keyword'])
  	
    updateKeyList(key)
    
    elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
      
    result = tweetmatch(elsr, str(key))
    retresult = parse(result)
    
    return render_template('tweet.html', result=retresult)


@application.route('/rtw', methods = ['GET','POST'])
def rtw():
  elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
  global chab
  if len(chab) is 0:
    result = elsr.search(size=5000,index='twitter')
  else:
    result = elsr.search(size=5000, index="twitter", body={"query": {"query_string": {"query": chab}}})

  return jsonify(parse(result))
  
  
@application.route("/")
def index():
  elsr = Elasticsearch([{'host':'search-twitter-es-mdmyclrn5jzxcopqx4houjyoo4.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
  result = elsr.search(size=5000,index='twitter')
  retresult = parse(result)
  return render_template('tweet.html', result=retresult)


  
if __name__ == "__main__":
	  application.run()