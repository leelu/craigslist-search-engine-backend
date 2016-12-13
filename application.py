from flask import Flask, render_template, json, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search, Q
#from urllib.request import urlopen
import json, requests

app = application= Flask(__name__)
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
        index="craigslist-index3",
        body={
            "size": 100,
          "query": {
            "query_string": {
              "query": searchterm,
              "fields": ["title", "description"]
            }
          }
        }
    )
    return response
    #for hit in response['hits']['hits']:
    #    print(hit['_score'], hit['_source']['link'])




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search')
def search():
    #print("search web method running")
    term = request.args.get('searchterm')
    #print(term)
    response = callElasticsearchAPI(term)

    result = formatResponse(response)
    #print(result)
    return result
    #Process result
    #for hit in response['hits']['hits']:
    #    print(hit['_score'], hit['_source']['title'])

    #for tag in response['aggregations']['per_tag']['buckets']:
    #    print(tag['key'], tag['max_lines']['value'])

    #return '<p>You entered: ' + term + '</p>'


def formatResponse(response):

    html = ''
    html += '<table border = "1">'

    for hit in response['hits']['hits']:
        #print(hit['_score'], hit['_source']['title'])
        #print("hit loop")
        score = hit['_score']
        link = hit['_source']['link']
        title = hit['_source']['title']
        description = hit['_source']['description']
        print("score: " + str(score), "link: " + link, "title: " + title)
        html += '<div class="result"><div class="title"><h4><a href="' + link + '">' + title + '</a></h4></div><div class="link">' + link + '</div><div>relevance score: <i>' + str(score) + '</i><p>' + description.replace('\n', ' ')[:200] + '</p></div></div>'


    return html

#def get_data():
#    response = requests.get("http://myhost/jsonapi")
#    ...
#    return response

if __name__ == '__main__':
    app.run()

