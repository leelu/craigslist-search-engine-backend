from flask import Flask, render_template, json, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search, Q
#from urllib.request import urlopen
import json, requests

application = app = Flask(__name__)
host = 'search-mysearchengine-7canadtuf2dlzoj5bvjeqwqufe.us-east-1.es.amazonaws.com'
awsauth = AWS4Auth('AKIAJL3TXNQWGSIHZ5LQ', '+OP3FeY1vIr4S6TDG6yZMSQRYL8oaxJyu4pSYFSQ', 'us-east-1', 'es')
esUrl = 'https://search-mysearchengine-7canadtuf2dlzoj5bvjeqwqufe.us-east-1.es.amazonaws.com/'

es = Elasticsearch(hosts=[{'host': host, 'port': 443}],
                                         http_auth=awsauth,
                                         use_ssl=True,
                                         verify_certs=True,
                                         connection_class=RequestsHttpConnection)


def callElasticsearchAPI(searchterm):

    #searchUrl = esUrl + "_search?q=" + searchterm
    #resp = requests.get(url=searchUrl)
    #data = json.loads(resp.text)
    #response = urlopen(esUrl)
    #data = json.loads(response.text)
    #return json.loads(data)


    response = es.search(
        index="craigslist-index",
        body={
          "query": {
            "query_string": {
              "query": searchterm,
              "fields": ["content"]
            }
          }
        }
    )

    for hit in response['hits']['hits']:
        print(hit['_score'], hit['_source']['link'])




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search')
def search():
    print("search web method running")
    term = request.args.get('searchterm')
    print(term)
    jsondata = callElasticsearchAPI(term)


    #Process result
    #for hit in response['hits']['hits']:
    #    print(hit['_score'], hit['_source']['title'])

    #for tag in response['aggregations']['per_tag']['buckets']:
    #    print(tag['key'], tag['max_lines']['value'])

    return '<p>You entered: ' + term + '</p>'


#def get_data():
#    response = requests.get("http://myhost/jsonapi")
#    ...
#    return response

if __name__ == '__main__':
    app.run()


