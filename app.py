from flask import Flask
from flask import Flask, render_template, request, jsonify, json
from flask_cors import CORS, cross_origin

import time

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route('/igtag', methods=['GET', 'POST'])
def igtag():
    from InstagramAPI import InstagramAPI
    if request.method == 'GET':
       username = request.args.get('user')
       password = request.args.get('pass')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    tag_search= request.args.get('tag')
    InstagramAPI.tagFeed(tag_search)
    time.sleep(1)
    result = InstagramAPI.LastJson
    
    #uncomment to get the full json response
    #jsonify(result) 

    #get latitude, longitude and label from location
    loc = []
   
    for lo in result["items"]:
       try:
          loc.append({"lat": lo['location']['lat'], "lng":lo['location']['lng'], "label": lo['location']['name']})
       except KeyError: 
              pass
       
    return jsonify(loc)

  



@app.route('/igloc', methods=['GET', 'POST'])
def igloc():
    from InstagramAPI import InstagramAPI
    if request.method == 'GET':
       username = request.args.get('user')
       password = request.args.get('pass')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    location = request.args.get('loc')
    locid = request.args.get('locid') 
    #search by name
    place= InstagramAPI.searchLocation(location)
    InstagramAPI.getLocationFeed(place)
    #search by location id
    if not location:
        InstagramAPI.getLocationFeed(locid)
    time.sleep(1)
    result = InstagramAPI.LastJson
     
    #uncomment to get the full json response
    #jsonify(result) 

    #get only latitude, longitude and label from location
    loc = []
    
    for lo in result["items"]:
        loc.append({"lat": lo['location']['lat'],"lng": lo['location']['lng'], "label": lo['location']['name']})
         
    return jsonify(loc)

@app.route('/igfollower', methods=['GET', 'POST'])
def igfollower():
    from InstagramAPI import InstagramAPI
    if request.method == 'GET':
       username = request.args.get('user')
       password = request.args.get('pass')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
    
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