#/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import urllib2
import time
import datetime
import math
import xml.etree.ElementTree as ET
import urlparse
import webbrowser
import pdb

import requests
from requests_oauthlib import OAuth1

import api_key as AK
import misc as MI

def oauth_requests():
    auth = OAuth1(AK.API_KEY, AK.SECRET_KEY, callback_uri=callback_uri)
    #print auth
    r = requests.post(request_url, auth=auth)
    #print r
    request_token = dict(urlparse.parse_qsl(r.text))
    #print request_token

    # Getting the User Authorization
    # ブラウザを開きOAuth認証確認画面を表示
    # ユーザーが許可するとPINコードが表示される
    url='{0}?oauth_token={1}&perms=write'.format(authorize_url,  request_token['oauth_token'])
    #print testurl
    browser=webbrowser.get(MI.BROWSER_PATH)
    browser.open(url)

    oauth_verifier = raw_input("[PIN Code]> ")  # 上記PINコードを入力する
    #print oauth_verifier
    auth = OAuth1(
            AK.API_KEY,
            AK.SECRET_KEY,
            request_token['oauth_token'],
            request_token['oauth_token_secret'],
            verifier=oauth_verifier)
    r = requests.post(access_token_url, auth=auth)

    access_token = dict(urlparse.parse_qsl(r.text))
    return access_token

class baseinfo():

    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.user_id = user_id
        self.api_url = 'https://api.flickr.com/services/rest/'

class user(baseinfo):

    def get_user_info(self):
        method = "method=flickr.people.getInfo"
        res_format = "format=rest"
        req_str = self.api_url + "?" + method + "&" + self.api_key + "&" + user_id + "&" + res_format
        request = urllib2.Request(req_str)
        response = urllib2.urlopen(request)
        res_data = response.read()
        #print res_data
        elem = ET.fromstring(res_data)
        self.username = elem.findtext(".//username")
        self.description = elem.findtext(".//description")
        self.photosurl = elem.findtext(".//photosurl")
        self.profileurl = elem.findtext(".//profileurl")
        self.mobileurl = elem.findtext(".//mobileurl")
        self.firstdatetaken = elem.findtext(".//firstdatetaken")
        self.firstdate = elem.findtext(".//firstdate")
        self.count = elem.findtext(".//count")

    def print_user_data(self):
        print u"username : {0}".format(self.username)
        print u"description : {0}".format(self.description)
        print u"photosurl : {0}".format(self.photosurl)
        print u"profileurl : {0}".format(self.profileurl)
        print u"mobileurl : {0}".format(self.mobileurl)
        print u"firstdatetaken : {0}".format(self.firstdatetaken)
        print u"firstdate : {0}".format(self.firstdate)
        print u"count : {0}".format(self.count)


class albums(baseinfo):

    def __init__(self, api_key, secret_key, user_id, oauth_key, oauth_secret):
        self.api_key = api_key
        self.secret_key = secret_key
        self.user_id = user_id
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret
        self.api_url = 'https://api.flickr.com/services/rest/'

    def get_albums_list(self):
        auth = OAuth1(self.api_key, self.secret_key,
                self.oauth_key, self.oauth_secret)
        param_dict = {
                "method" : "flickr.photosets.getList",
                "user_id" : self.user_id,
                "format" : "rest"
                }
        response = requests.get(self.api_url, params=param_dict, auth=auth)
        #print response.text
        res_data = response.text.encode('utf-8')

        elem = ET.fromstring(res_data)
        # albums info
        albums_info = elem.find("photosets")
        self.page = albums_info.get("page")
        self.pages = albums_info.get("pages")
        self.perpage = albums_info.get("perpage")
        self.total = albums_info.get("total")
        # album info
        album_info = elem.findall(".//photoset")
        self.album_list = []
        for ai in album_info:
            album_id = ai.get("id")
            self.album_list.append(album_id)
            #title = ai.findtext("title")
            #description = ai.findtext("description")
            #album_photos = ai.get("photos")
            #album_vcss = ai.get("visibility_can_see_set")
            #album_videos = ai.get("videos")
            #album_farm = ai.get("farm")
            #album_dateupdate = ai.get("date_update")
            #album_datecreate = ai.get("date_create")
            #album_primary = ai.get("primary")
            #album_server = ai.get("server")
            #album_ni = ai.get("needs_interstitial")
            #album_count_comments = ai.get("count_comments")
            #album_count_views = ai.get("count_views")
            #album_can_comment = ai.get("can_comment")
            #album_secret = ai.get("secret")

    def print_albums_info(self):
        print "page : {0}".format(self.page)
        print "pages : {0}".format(self.pages)
        print "perpage : {0}".format(self.perpage)
        print "total : {0}".format(self.total)

    def get_album_info(self, album_id):
        #print ".",
        auth = OAuth1(self.api_key, self.secret_key,
                self.oauth_key, self.oauth_secret)
        param_dict = {
                "method" : "flickr.photosets.getInfo",
                "user_id" : self.user_id,
                "photoset_id" : album_id,
                "format" : "rest"
                }
        response = requests.get(self.api_url, params=param_dict, auth=auth)
        #print response.text
        res_data = response.text.encode('utf-8')

        elem = ET.fromstring(res_data)
        # album info
        album_info = elem.findall(".//photoset")
        self.photoset = {}
        #print "album_id : {0}".format(album_id)
        for ai in album_info:
            album_title = ai.findtext("title")
            album_description = ai.findtext("description")
            album_owner = ai.get("owner")
            album_primary = ai.get("primary")
            album_secret = ai.get("secret")
            album_server = ai.get("server")
            album_farm = ai.get("farm")
            album_photo_count = ai.get("photos")
            album_count_views = ai.get("count_views")
            album_count_comments = ai.get("count_comments")
            album_count_videos = ai.get("videos")
            album_can_comment = ai.get("can_comment")
            album_dateupdate = ai.get("date_update")
            update_date = datetime.datetime.fromtimestamp(int(album_dateupdate))
            ud = update_date.strftime("%Y-%m-%d %H:%M:%S")
            album_datecreate = ai.get("date_create")
            create_date = datetime.datetime.fromtimestamp(int(album_datecreate))
            cd = create_date.strftime("%Y-%m-%d %H:%M:%S")
            self.photoset[album_id] = {
                    "title" : album_title,
                    "description" : album_description,
                    "owner" : album_owner,
                    "primary_photo_id" : album_primary,
                    "secret" : album_secret,
                    "server" : album_server,
                    "farm" : album_farm,
                    "photos" : album_photo_count,
                    "views_count" : album_count_views,
                    "comments_count" : album_count_comments,
                    "videos" : album_count_videos,
                    "update_date" : ud,
                    "create_date" : cd,
                    }

            def print_album_info(self, album_id):
                print u"title : {0}".format(self.photoset[album_id]["title"])
                print u"description : {0}".format(self.photoset[album_id]["description"])
                print "owner : {0}".format(self.photoset[album_id]["owner"])
                print "primary : {0}".format(self.photoset[album_id]["primary"])
                print "secret : {0}".format(self.photoset[album_id]["secret"])
                print "server : {0}".format(self.photoset[album_id]["server"])
                print "farm : {0}".format(self.photoset[album_id]["farm"])
                print "photos : {0}".format(self.photoset[album_id]["photos"])
                print "videos : {0}".format(self.photoset[album_id]["count_videos"])
                print "views : {0}".format(self.photoset[album_id]["count_views"])
                print "comments : {0}".format(self.photoset[album_id]["count_comments"])

    def get_photos_list(self, album_id):
        auth = OAuth1(self.api_key, self.secret_key,
                self.oauth_key, self.oauth_secret)
        param_dict = {
                "method" : "flickr.photosets.getPhotos",
                "user_id" : self.user_id,
                "photoset_id" : album_id,
                "format" : "rest"
                }
        response = requests.get(self.api_url, params=param_dict, auth=auth)
        #print response.text
        res_data = response.text.encode('utf-8')

        #print res_data
        elem = ET.fromstring(res_data)
        # album info
        photos_info = elem.findall(".//photo")
        self.photos_list = { album_id : [] }
        for pi in photos_info:
            photo_id = pi.get("id")
            #print "photo_id: {0}".format(photo_id)
            self.photos_list[album_id].append(photo_id)
            break

    def print_photos_list(self, album_id):
        print "ALBUM ID : {0}".format(album_id)
        print u"ALBUM NAME : {0}".format(self.photoset[album_id]["title"])
        print "ALBUM IN PHOTS > "
        for pl in self.photos_list[album_id]:
            print pl

    def get_photo_tag(self, photo_id):
        auth = OAuth1(self.api_key, self.secret_key,
                self.oauth_key, self.oauth_secret)
        param_dict = {
                "method" : "flickr.photos.getInfo",
                "user_id" : self.user_id,
                "photo_id" : photo_id,
                "format" : "rest"
                }
        response = requests.get(self.api_url, params=param_dict, auth=auth)
        #print response.text
        res_data = response.text.encode('utf-8')

        elem = ET.fromstring(res_data)
        # album info
        photo_tags = elem.find(".//tags")
        tagstr = ''
        for pt in photo_tags:
            tags = pt.itertext()
            for t in tags:
                tagstr += t

        return tagstr

    def sort_album_exe(self, photoset_ids):
        #print "album_id list {0}".format(photoset_ids)
        #t = time.time()
        #cb = math.floor(t)
        auth = OAuth1(self.api_key, self.secret_key,
                self.oauth_key, self.oauth_secret)
        param_dict = {
                "method" : "flickr.photosets.orderSets",
                "photoset_ids" : photoset_ids,
                #"cb" : cb,
                "format" : "rest"
                }
        #print param_dict
        response = requests.post(self.api_url, data=param_dict, auth=auth)
        #print response
        res_data = response.text.encode('utf-8')
        print res_data

        def print_info(self):
            print self

def sort_album(list_album, way, ad):

    #id,title,update_date,create_date,views,tag

    if way == "tag":
        sorted_list = sorted(list_album, key=lambda album: album["album_tag"], reverse=ad)
    elif way == "id":
        sorted_list = sorted(list_album, key=lambda album: album["album_idx"], reverse=ad)
    elif way == "title":
        sorted_list = sorted(list_album, key=lambda album: album["album_title"],
                reverse=ad)
    elif way == "views_count":
        sorted_list = sorted(list_album, key=lambda album: album["view_count"], reverse=ad)
    elif way == "update_date":
        sorted_list = sorted(list_album, key=lambda album: album["update_date"],
                reverse=ad)
    elif way == "create_date":
        sorted_list = sorted(list_album, key=lambda album: album["create_date"],
                reverse=ad)
    else:
        print "No Way"

    sorted_album_id_list = []
    #print sorted_list
    #print len(sorted_list)
    #print type(sorted_list)
    for sl in sorted_list:
        #print sl["album_id"]
        sorted_album_id_list.append(str(sl["album_id"]))

    return sorted_album_id_list

request_url = 'https://www.flickr.com/services/oauth/request_token'
authorize_url = 'https://www.flickr.com/services/oauth/authorize'
access_token_url = 'https://www.flickr.com/services/oauth/access_token'
access_url = 'https://api.flickr.com/services/rest/'
callback_uri = 'oob'

if __name__ == '__main__' :
    # Input Sort Key
    if len(sys.argv) != 2:
        print "Usage: {0} {1} {2}".format("python2",
                "flickr_album_sort.py", "{sort key}")
        # print prompt
        print "sort ? {0} {1} {2} {3} {4} {5} or {6}".format("id", "title",
        "update_date", "create_date", "views_count", "tag", "exit")
        sort_key = raw_input("[sort_key]>")
        if sort_key == "exit":
            exit()
    elif len(sys.argv) == 2:
        #id,title,update_date,create_date,views,tag
        sort_key = sys.argv[1] or ""

    enable_sort_keys = ("id", "title", "update_date",
            "create_date", "views_count", "tag")
    if not (sort_key in enable_sort_keys):
        print "[Bat sort key]: {0}".format(sort_key)
        print "Program exit"
        exit()
    print "[sort] > {0}".format(sort_key)
    # get access token
    access_token = oauth_requests()
    resource_owner_key = access_token.get('oauth_token')
    resource_owner_secret = access_token.get('oauth_token_secret')
    #print resource_owner_key
    #print resource_owner_secret
    my_albums = albums(AK.API_KEY, AK.SECRET_KEY, MI.USER_ID,
            resource_owner_key,
            resource_owner_secret)

    my_albums.get_albums_list()
    my_albums.print_albums_info()

    photo_list = []
    LOADING_CHAR = [ "    ", ".", ".o", ".oO", ".oO0" ]
    loading_i = 0
    #pdb.set_trace()
    for album_id in my_albums.album_list:
        sys.stdout.write("\r[{0:d}]{1} {2}".format(loading_i, "...",
            LOADING_CHAR[loading_i % len(LOADING_CHAR)]))
        sys.stdout.flush()
        ignore_flag = False
        for ignore_id in MI.IGNORE_SORT_ALBUM_LIST:
            if album_id == ignore_id:
                ignore_flag = True
                break
        if ignore_flag == True:
            loading_i += 1
            continue
        my_albums.get_album_info(album_id)
        #my_albums.print_album_info(album_id)
        #my_albums.get_photos_list(album_id)
        #my_albums.print_photos_list(album_id)
        #photo_id = my_albums.photos_list[album_id][0]

        if sort_key == "id":
            ### id case
            photo_list.append({
               'album_id' : album_id,
               'album_idx' : album_id,
               })
        elif sort_key == "title":
            ### Title case
            album_title = my_albums.photoset[album_id]["title"]
            photo_list.append({
                'album_id' : album_id,
                'album_title' : album_title,
                })
        elif sort_key == "update_date":
            ### date update case
            update_date = my_albums.photoset[album_id]["update_date"]
            photo_list.append({
                'album_id' : album_id,
                'update_date' : update_date,
                })
        elif sort_key == "create_date":
            ### date create case
            create_date = my_albums.photoset[album_id]["create_date"]
            photo_list.append({
                'album_id' : album_id,
                'create_date' : create_date,
                })
        elif sort_key == "views_count":
            ### view case
            view_count = my_albums.photoset[album_id]["views_count"]
            photo_list.append({
                'album_id' : album_id,
                'view_count' : view_count,
                })
        elif sort_key == "tag":
            ### Tag case
            photo_id = my_albums.photoset[album_id]["primary_photo_id"]
            album_tag = my_albums.get_photo_tag(photo_id)
            photo_list.append({
                'album_id' : album_id,
                'album_tag' : album_tag,
                })
        else:
            # No case
            #id,title,update_date,create_date,views,tag
            print "\n Please input sort key > {0} or {1} or {2} or {3} or {4}".format("id", "title", "update_date",
                    "create_date", "views_count", "tag")
            exit()

        loading_i += 1

    print ""
    lst = sort_album(photo_list, sort_key, True)

    # List copy
    ignores = MI.IGNORE_SORT_ALBUM_LIST[:]
    # Mix album list
    mix_album_list = ignores + lst

    sort_ids = ',' . join([str(m) for m in mix_album_list])
    #sort_ids = ""
    #for l in lst:
    #    sort_ids += l

    print "album sort start >"
    my_albums.sort_album_exe(sort_ids)
    print "< album sort done"
