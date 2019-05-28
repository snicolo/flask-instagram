
from flask import Flask, render_template, request, jsonify, json
from flask_cors import CORS, cross_origin

import time

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
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
        username = request.values.get('user')
        password = request.values.get('passw')
        tag = request.values.get('tag')
    
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
          loc.append({"lat": lo['location']['lat'], "lng":lo['location']['lng'], "label": lo['location']['name'], "username": lo['user']['username']})
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
    place=InstagramAPI.searchLocation(location)
    InstagramAPI.getLocationFeed(place)
    #search by location id
    if not location:
        InstagramAPI.getLocationFeed(locid)
    time.sleep(1)
    result = InstagramAPI.LastJson
    
  
     
    
    #uncomment to get the full json response
    #return jsonify(result) 

    #get only latitude, longitude and label from location
    loc = []
    
    for lo in result['items']:
        loc.append({"lat": lo['location']['lat'],"lng": lo['location']['lng'], "label": lo['location']['name'],"address": lo['location']['address']})
         
    return jsonify(loc)


@app.route('/igfoll', methods=['GET', 'POST'])
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
    #get followers
    followers   = []
    next_max_id = True
    while next_max_id:
     print (next_max_id)
 
     if next_max_id == True: next_max_id=''
     _ = InstagramAPI.getUserFollowers(username_id,maxid=next_max_id)
     followers.extend ( InstagramAPI.LastJson.get('users',[]))
     next_max_id = InstagramAPI.LastJson.get('next_max_id','')
     time.sleep(1)
    
    followers_list=followers
    
    
    flwe=[]
    #filter full name and username in followers list
    for name in followers_list:
        flwe.append({"username": name['username'], "fullname": name['full_name']})

    #get followings
    followings   = []
    next_max_id = True
    while next_max_id:
     print (next_max_id)
 
     if next_max_id == True: next_max_id=''
     _ = InstagramAPI.getUserFollowings(username_id,maxid=next_max_id)
     followings.extend ( InstagramAPI.LastJson.get('users',[]))
     next_max_id = InstagramAPI.LastJson.get('next_max_id','')
     time.sleep(1)
    
    flwi=[]
    followings_list=followings

    #filter full name and username in followings list
    for name in followings_list:
        flwi.append({"username": name['username'], "fullname": name['full_name']})
       
   

    foll=[]

    foll.append({"following": flwi, "follower":flwe})

    return jsonify(foll)


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
    #filter info about user
    username_id = InstagramAPI.LastJson["user"]["pk"]
    x =InstagramAPI.LastJson["user"]["full_name"]
    n =InstagramAPI.LastJson["user"]["biography"]
    y = InstagramAPI.LastJson["user"]["follower_count"]
    z = InstagramAPI.LastJson["user"]["following_count"]
    
    
    

    result= InstagramAPI.getTotalUserFeed(username_id)
    
    time.sleep(2)
    
    loc = [{"name": x, "bio": n, "followers": y, "followings": z}]
    #filter lat, lng, label and time
    for u in result:
       try:
        loc.append({"lat": u['location']['lat'], "lng":u['location']['lng'], "label": u['location']['name'], "time": u['taken_at']})
       except KeyError: 
              pass
    
    return jsonify(loc)


        
if __name__ == "__main__":
    app.run()
