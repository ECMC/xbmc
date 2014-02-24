
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

class PicturesWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid = kwargs.get("menuid") or ""
	
	def loadContentForAlbum( self, li ):
		try:
			head = self.getControl(50)
			head.setLabel(li.getLabel())
			albumid = li.getProperty("albumid")
		
			self.grid = self.getControl(205)
			while self.grid.size() > 0 :
				self.grid.removeItem(0)

			json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"PictureLibrary.GetVideos","id":1,"params": {"properties":["title","album","face","location","thumbnail"],"filter":{"albumid":'+str(albumid)+'}}}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			if jsonobject['result'].has_key('pictures'):
				print "Found pictures"
				for item in reversed(jsonobject['result']['pictures']):
					print "adding "+item.get('label','')
					li = xbmcgui.ListItem(label=item.get('label',''), iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("label",str(item.get('label','')))
					self.grid.addItem(li)


					#li = self.grid.addItem(xbmcgui.ListItem(label='', iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path=''))
					#li.setProperty("label",item.get('label',''))
		except:
			print_exec()
	
	def onInit( self ):
		try:
			self.setFocus( self.getControl(int(self.menuid) ) )
		
			json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PictureLibrary.GetVideoAlbums", "params": { "properties": [ "face", "location", "thumbnail"], "filter" : {"picturetype": "Video"}, "sort": { "order": "ascending", "method": "album", "ignorearticle": true } }, "id": "libPictureAlbums"}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			self.list = self.getControl(105)
			if jsonobject['result'].has_key('picturealbums'):
				for item in reversed(jsonobject['result']['picturealbums']):
					li = xbmcgui.ListItem(label=item.get('label',''), iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("albumid",str(item.get('albumid','')))
					self.list.addItem(li)
			
			#self.loadContentForAlbum( self.list.getListItem(0) )
		except:
			print_exec()

	def onFocus( self, controlID ):
		pass

	def onClick( self, controlID ):
		print str(controlID)
		#load the album
		li = self.list.getSelectedItem()
		if controlID == 105:
			self.list = self.getControl(controlID)
			self.loadContentForAlbum( li )
		#start the slide show
		if controlID == 205:
			self.grid = self.getControl(controlID)
			video = self.grid.getSelectedItem()
			self.playVideo( video )
		
	def playVideo(self, video):
		path = "/Users/ashokjaiswal/Videos/"#video.getProperty("path")
		file = video.getProperty("label")
		playfile = path+video.getProperty("label")
		
		print "-------------------------------"
		print "Play video for path "
		print playfile
		print "-------------------------------"
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()
		#playlist.add(path+video.getProperty("label"))
		playlist.add(playfile)
		xbmc.Player().play( playlist)
        
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
    w = PicturesWindow( "custom_ezee_videos.xml", __addonDir__, menuid=menuid )
    w.doModal()
    del w

if ( __name__ == "__main__" ):
	params=get_params()
	heading = __addonName__
	loadPictureAlbums(params["buttonid"])