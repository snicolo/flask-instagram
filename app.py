from flask import Flask
from flask import Flask, render_template, request, jsonify, json

import time

app = Flask(__name__)

@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route('/igtag', methods=['get'])
def igtag():
    from InstagramAPI import InstagramAPI
    username = request.args.get('user')
    password = request.args.get('pass')
    tag_search = request.args.get('tag')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    
    InstagramAPI.getHashtagFeed(tag_search)
    time.sleep(1)
    result1 = InstagramAPI.LastJson
    #print(result)
    return jsonify(result1)

@app.route('/igloc', methods=['get'])
def igloc():
    from InstagramAPI import InstagramAPI
    username = request.args.get('user')
    password = request.args.get('pass')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    location = request.args.get('loc')
    InstagramAPI.getLocationFeed(location)
    time.sleep(1)
    result = InstagramAPI.LastJson
    #print(result)
    return jsonify(result)
         

if __name__ == "__main__":
    app.run()