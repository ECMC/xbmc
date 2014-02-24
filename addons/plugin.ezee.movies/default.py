
# Modules general
import os
import sys
import simplejson, json
from traceback import print_exc

# Modules XBMC
import xbmc, xbmcgui, sqlite3
from xbmcaddon import Addon


__settings__  = Addon( "script.module.dialogaddonscan" )
__addonName__ = __settings__.getAddonInfo( "name" )
__addonDir__  = __settings__.getAddonInfo( "path" )

class MovieDetailsWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid =  kwargs.get("menuid") or ""
		self.movieid =  kwargs.get("movieid") or ""
		
		json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": {"field": "playcount", "operator": "is", "value": "0"}, "properties" : ["art", "rating", "thumbnail", "playcount", "file", "plot", "year", "trailer", "runtime", "genre"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}')
		json_query = unicode(json_query, 'utf-8', errors='ignore')
		self.jsonobject = simplejson.loads(json_query)
		
	def onInit(self):
		self.loadMovie(self.movieid)

	def loadMovie( self, movieid):
		try:
			#fill the similar images box
			self.similar_list = self.getControl(305)
			if self.jsonobject['result'].has_key('movies'):
				for item in self.jsonobject['result']['movies']:
					li = xbmcgui.ListItem(label='', iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("movieid",str(item.get('movieid','')))
					self.similar_list.addItem(li)
		
			self.movieid = movieid
			json_query = xbmc.executeJSONRPC('{"method":"VideoLibrary.GetMovieDetails","id":-1147449918,"jsonrpc":"2.0","params":{"movieid":'+str(movieid)+',"properties":["year","playcount","rating","thumbnail","genre","runtime","studio","director","plot","mpaa","votes","cast","file","fanart","resume","trailer","art"]}}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			if jsonobject['result'].has_key('moviedetails'):
				print "found movie"
				item = jsonobject['result']['moviedetails']

				self.getControl(59).setImage(item.get('fanart',''))	
				self.getControl(60).setImage(item.get('thumbnail',''))	
				self.getControl(50).setLabel(item.get('label','')+"   ("+str(item.get('year',''))+")")
				self.getControl(80).setLabel(str(item.get('runtime','')))
				self.getControl(78).setLabel(item.get('plot',''))
				print item.get('plot','')
				for item in jsonobject['result']['moviedetails']:
					text = "Director: "
					for director in jsonobject['result']['moviedetails']['director']:
						text = text + director + " "
					self.getControl(76).setLabel(text)
					text = "Genre: "
					for genre in jsonobject['result']['moviedetails']['genre']:
						text = text + genre + " "
					self.getControl(75).setLabel(text)
					text = "Cast: "
					for cast in jsonobject['result']['moviedetails']['cast']:
						text = text + cast + " "
					self.getControl(77).setLabel("text")
		except:
			print_exec()
			
	def onClick( self, controlID ):
		print "Control ID is " + str(controlID)
		if controlID == 62: #last movie
			foundmovie = False
			if self.jsonobject['result'].has_key('movies'):
				for item in reversed(self.jsonobject['result']['movies']):
					lastmovieid = item.get('movieid','')
					print item.get('movieid','')
					print "compare to "+str(self.movieid)
					if foundmovie:
						self.loadMovie( item.get('movieid','') )
						break
					foundmovie = str(self.movieid) == str(item.get('movieid',''))
			
		if controlID == 64: #next movie
			foundmovie = False
			if self.jsonobject['result'].has_key('movies'):
				for item in self.jsonobject['result']['movies']:
					print item.get('movieid','')
					print "compare to "+str(self.movieid)
					if foundmovie:
						self.loadMovie( item.get('movieid','') )
						break
					foundmovie = str(self.movieid) == str(item.get('movieid',''))
					
		if controlID == 305:
			self.similar_list = self.getControl(305)
			li = self.similar_list.getSelectedItem()
			self.loadMovie( li.getProperty("movieid") )
			
		if controlID == 105:
			print controlID
			print '{"jsonrpc": "2.0", "method": "XBMC.Play","params":{"movieid":'+str(self.movieid)+'},"id":1}'
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Player.Open","id":1,"params":{"item":{"movieid":'+str(self.movieid)+'}}}')
		if controlID == 79:
			print controlID
			print '{"jsonrpc": "2.0", "method": "XBMC.Play","params":{"movieid":'+str(self.movieid)+'},"id":1}'
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Player.Open","id":1,"params":{"item":{"movieid":'+str(self.movieid)+'}}}')
			#xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "XBMC.Play","params":{"movieid":'+cstr(self.movieid)+'},"id":1}')
			
			
class PicturesWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid = kwargs.get("menuid") or ""

	
	def onInit( self ):
		try:
			self.setFocus( self.getControl(int(self.menuid) ) )
		
			json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": {"field": "playcount", "operator": "is", "value": "0"}, "properties" : ["art", "rating", "thumbnail", "playcount", "file", "plot", "year", "trailer", "runtime", "genre"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			self.list = self.getControl(105)
			while self.list.size() > 0 :
				self.list.removeItem(0)

			if jsonobject['result'].has_key('movies'):
				for item in jsonobject['result']['movies']:
					li = xbmcgui.ListItem(label='', iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("movieid",str(item.get('movieid','')))
					li.setProperty("label",str(item.get('label','')))
					self.list.addItem(li)
			
		except:
			print_exec()

	def onFocus( self, controlID ):
		pass

	def onClick( self, controlID ):
		self.list = self.getControl(105)
		li = self.list.getSelectedItem()
		w = MovieDetailsWindow( "custom_ezee_movie_details.xml", __addonDir__, menuid = self.menuid, movieid=li.getProperty("movieid") )
		w.doModal()
		del w


	def onAction( self, action ):
		print "onAction"
		print action
		if action in [ 9, 10, 117 ]:
			self.close()

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def loadPictureAlbums(menuid):
    w = PicturesWindow( "custom_ezee_movies.xml", __addonDir__, menuid=menuid )
    w.doModal()
    del w

if ( __name__ == "__main__" ):
	params=get_params()
	heading = __addonName__
	loadPictureAlbums(params["buttonid"])