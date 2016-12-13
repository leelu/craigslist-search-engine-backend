from flask import Flask, render_template, json, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


app = application = Flask(__name__)
host = 'search-mysearchengine-7canadtuf2dlzoj5bvjeqwqufe.us-east-1.es.amazonaws.com'
awsauth = AWS4Auth('AKIAJL3TXNQWGSIHZ5LQ', '+OP3FeY1vIr4S6TDG6yZMSQRYL8oaxJyu4pSYFSQ', 'us-east-1', 'es')
esUrl = 'https://search-mysearchengine-7canadtuf2dlzoj5bvjeqwqufe.us-east-1.es.amazonaws.com/'

es = Elasticsearch(hosts=[{'host': host, 'port': 443}],
                                         http_auth=awsauth,
                                         use_ssl=True,
                                         verify_certs=True,
                                         connection_class=RequestsHttpConnection)


def callElasticsearchAPI(searchterm):

    response = es.search(
        index="craigslist-index",
        body={
            "size": 1000,
          "query": {
            "query_string": {
              "query": searchterm,
              "fields": ["title", "description"]
            }
          }
        }
    )
    return response



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search')
def search():

    term = request.args.get('searchterm')

    response = callElasticsearchAPI(term)

    result = formatResponse(response)

    return result


def formatResponse(response):

    html = ''
    html += '<p class="stat">'  + str(response['hits']['total']) + ' results genereated in ' + str(response['took']) + ' ms</p>'

    for hit in response['hits']['hits']:

        score = hit['_score']
        link = hit['_source']['link']
        title = hit['_source']['title']
        description = hit['_source']['description']
        print("score: " + str(score), "link: " + link, "title: " + title)
        html += '<div class="result"><div class="title"><h4><a target="_blank" href="' + link + '">' + title + '</a></h4></div><div class="link">' + link + '</div><div>relevance score: <i>' + str(score) + '</i><p>' + description.replace('\n', ' ')[:200] + '</p></div></div>'


    return html

if __name__ == '__main__':
    app.run()

