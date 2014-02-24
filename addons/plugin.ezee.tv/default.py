
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

class TvShowDetailsWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid =  kwargs.get("menuid") or ""
		self.tvshowid =  kwargs.get("tvshowid") or ""
		
		json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": {"field": "playcount", "operator": "is", "value": "0"}, "properties": ["art", "genre", "plot", "title", "originaltitle", "year", "rating", "thumbnail", "playcount", "file", "fanart"], "sort": { "order": "ascending", "method": "label" } }, "id": "libTvShows"}')
		json_query = unicode(json_query, 'utf-8', errors='ignore')
		self.jsonobject = simplejson.loads(json_query)
		
	def onInit(self):
		self.loadTvShow(self.tvshowid)

	def loadTvShow( self, tvshowid):
		try:
			print "loading tv shows for id"+str(tvshowid)
			self.tvshowid = tvshowid
			json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"VideoLibrary.GetSeasons","id":1,"params":{"properties":["season","showtitle","playcount","episode","thumbnail","fanart"],"tvshowid":'+str(tvshowid)+'}}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			if self.jsonobject['result'].has_key('tvshows'):
				for item in self.jsonobject['result']['tvshows']:
					if str(item.get('tvshowid',''))==str(tvshowid):
						print "fond tv show, populating"
						self.getControl(59).setImage(item.get('fanart',''))	
						self.getControl(60).setImage(item.get('thumbnail',''))	
						self.getControl(50).setLabel(item.get('label','')+"   ("+str(item.get('year',''))+")")
						#self.getControl(74).setLabel(str(item.get('runtime','')))
						self.getControl(78).setLabel(item.get('plot',''))

		except:
			print_exec()
			
	def onClick( self, controlID ):
	
		if controlID == 62: #last movie
			foundmovie = False
			if self.jsonobject['result'].has_key('tvshows'):
				for item in reversed(self.jsonobject['result']['tvshows']):
					lasttvshowid = item.get('tvshowid','')
					print item.get('tvshowid','')
					print "compare to "+str(self.tvshowid)
					if foundmovie:
						self.loadTvShow( item.get('tvshowid','') )
						break
					foundmovie = str(self.tvshowid) == str(item.get('tvshowid',''))
			
		if controlID == 64: #next movie
			foundmovie = False
			if self.jsonobject['result'].has_key('tvshows'):
				for item in self.jsonobject['result']['tvshows']:
					print item.get('tvshowid','')
					print "compare to "+str(self.tvshowid)
					if foundmovie:
						self.loadTvShow( item.get('tvshowid','') )
						break
					foundmovie = str(self.tvshowid) == str(item.get('tvshowid',''))


class PicturesWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid = kwargs.get("menuid") or ""
	
	def onInit( self ):
		try:
			self.setFocus( self.getControl(int(self.menuid) ) )
		
			json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": {"field": "playcount", "operator": "is", "value": "0"}, "properties": ["art", "genre", "plot", "title", "originaltitle", "year", "rating", "thumbnail", "playcount", "file", "fanart"], "sort": { "order": "ascending", "method": "label" } }, "id": "libTvShows"}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			self.list = self.getControl(105)
			while self.list.size() > 0 :
				self.list.removeItem(0)
			if jsonobject['result'].has_key('tvshows'):
				for item in jsonobject['result']['tvshows']:
					li = xbmcgui.ListItem(label=item.get('label',''), iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("tvshowid",str(item.get('tvshowid','')))
					li.setProperty("label",str(item.get('label','')))
					self.list.addItem(li)
		except:
			print_exec()

	def onFocus( self, controlID ):
		pass

	def onClick( self, controlID ):
		self.list = self.getControl(105)
		li = self.list.getSelectedItem()
		w = TvShowDetailsWindow( "custom_ezee_tv_details.xml", __addonDir__, menuid = self.menuid, tvshowid=li.getProperty("tvshowid") )
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
    w = PicturesWindow( "custom_ezee_tv.xml", __addonDir__, menuid=menuid )
    w.doModal()
    del w

if ( __name__ == "__main__" ):
	params=get_params()
	heading = __addonName__
	loadPictureAlbums(params["buttonid"])