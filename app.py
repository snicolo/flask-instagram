
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
       tag = request.args.get('tag')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
        tag = request.values.get('tags')
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    tag_search= tag
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
       location = request.args.get('loc')
       locid = request.args.get('locid') 
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
        location = request.values.get('locs')
        locid = request.values.get('locids')
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    
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
       usertofind = request.args.get('usertofind')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
        usertofind = request.values.get('usertofinds')
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    user_name = usertofind
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


@app.route('/igfollowing', methods=['GET', 'POST'])
def igfollowing():
    from InstagramAPI import InstagramAPI
    if request.method == 'GET':
       username = request.args.get('user')
       password = request.args.get('pass')
       usertofind = request.args.get('usertofind')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
        usertofind = request.values.get('usertofind')
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()
    user_name = usertofind
    InstagramAPI.searchUsername(user_name)
    username_id = InstagramAPI.LastJson["user"]["pk"]

    followings   = []
    next_max_id = True
    while next_max_id:
     print next_max_id
 
     if next_max_id == True: next_max_id=''
     _ = InstagramAPI.getUserFollowings(username_id,maxid=next_max_id)
     followings.extend ( InstagramAPI.LastJson.get('users',[]))
     next_max_id = InstagramAPI.LastJson.get('next_max_id','')
     time.sleep(1)
    
    followings_list=followings
    
    return jsonify(followings_list)


@app.route('/igfeed', methods=['GET', 'POST'])
def igfeed():
    from InstagramAPI import InstagramAPI
    if request.method == 'GET':
       username = request.args.get('user')
       password = request.args.get('pass')
       usertofind = request.args.get('usertofind')
    else:
        username = request.values.get('users')
        password = request.values.get('passws')
    
    InstagramAPI = InstagramAPI(username, password)
    InstagramAPI.login()

    user_name = usertofind
    InstagramAPI.searchUsername(user_name)
    username_id = InstagramAPI.LastJson["user"]["pk"]
   
    result= InstagramAPI.getTotalUserFeed(username_id)
    time.sleep(2)
    
    

    loc = []
    for u in result:
       try:
        loc.append({"lat": u['location']['lat'], "lng":u['location']['lng'], "label": u['location']['name']})
       except KeyError: 
              pass

    
    return jsonify(loc)


        
if __name__ == "__main__":
    app.run()
