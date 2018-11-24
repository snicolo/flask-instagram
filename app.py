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
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    tag_search= request.args.get('tag')
    InstagramAPI.getHashtagFeed(tag_search)
    time.sleep(1)
    result = InstagramAPI.LastJson
    #print(result)
    return jsonify(result)

@app.route('/igloc', methods=['get'])
def igloc():
    from InstagramAPI import InstagramAPI
    username = request.args.get('user')
    password = request.args.get('pass')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    location = request.args.get('loc')
    place= InstagramAPI.searchLocation(location)
    InstagramAPI.getLocationFeed(place)
    time.sleep(1)
    result = InstagramAPI.LastJson
    #print(result)
    return jsonify(result)

@app.route('/igfollower', methods=['get'])
def igfollower():
    from InstagramAPI import InstagramAPI
    username = request.args.get('user')
    password = request.args.get('pass')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    user_name = request.args.get('username')
    InstagramAPI.searchUsername(user_name)
    username_id = InstagramAPI.LastJson["user"]["pk"]

    followers   = []
    next_max_id = True
    while next_max_id:
     print next_max_id
 
     if next_max_id == True: next_max_id=''
     _ = InstagramAPI.getUserFollowers(username_id,maxid=next_max_id)
     followers.extend ( InstagramAPI.LastJson.get('users',[]))
     next_max_id = InstagramAPI.LastJson.get('next_max_id','')
     time.sleep(1)
    
    followers_list=followers
    return jsonify(followers_list)

if __name__ == "__main__":
    app.run()