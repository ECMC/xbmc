
# Modules general
import shutil
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
__addonID__  = __settings__.getAddonInfo( "id" )

class PictureSlideShowWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid =  kwargs.get("menuid") or ""
		self.albumid =  kwargs.get("albumid") or ""
	def onInit(self):
		self.preview = self.addControl(xbmcgui.ControlImage(742,216,1080,818, 'ezee/ezee_logo.png'))
		#self.preview = self.getControl("35")
		json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"PictureLibrary.GetPictures","id":1,"params": {"properties":["title","album","face","location","thumbnail"], "filter":{"albumid":'+str(self.albumid)+'}}}')
		json_query = unicode(json_query, 'utf-8', errors='ignore')
		jsonobject = simplejson.loads(json_query)
		if jsonobject['result'].has_key('pictures'):
			for item in reversed(jsonobject['result']['pictures']):
				self.preview.setImage('ezee/ezee_logo.png')
				#self.grid.addItem(xbmcgui.ListItem(label='', iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path=''))
    
      
class PicturesWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid =  kwargs.get("menuid") or ""
	
	def loadContentForAlbum( self, li ):
		try:
			head = self.getControl(50)
			head.setLabel(li.getLabel())
			albumid = li.getProperty("albumid")
		
			self.grid = self.getControl(205)
			while self.grid.size() > 0 :
				self.grid.removeItem(0)

			json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"PictureLibrary.GetPictures","id":1,"params": {"properties":["title","album","face","location","thumbnail"], "filter":{"albumid":'+str(albumid)+'}}}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			if jsonobject['result'].has_key('pictures'):
				print "Found pictures"
				for item in reversed(jsonobject['result']['pictures']):
					li = xbmcgui.ListItem(label='', iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("path",str(item.get('thumbnail','')))
					self.grid.addItem(li)
		except:
			print_exec()
	
	def onInit( self ):
		try:
			self.setFocus( self.getControl(int(self.menuid) ) )
		
			json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PictureLibrary.GetPictureAlbums", "params": { "properties": [ "face", "location", "thumbnail"], "filter" : {"picturetype": "Picture"}, "sort": { "order": "ascending", "method": "album", "ignorearticle": true } }, "id": "libPictureAlbums"}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			self.list = self.getControl(105)
			if jsonobject['result'].has_key('picturealbums'):
				for item in jsonobject['result']['picturealbums']:
					li = xbmcgui.ListItem(label=item.get('label',''), iconImage=item.get('thumbnail',''), thumbnailImage=item.get('thumbnail',''), path='')
					li.setProperty("albumid",str(item.get('albumid','')))
					self.list.addItem(li)
			
			#self.loadContentForAlbum( self.list.getListItem(0) )
		except:
			print_exec()

	def onFocus( self, controlID ):
		pass

	def onClick( self, controlID ):
		#load the album
		li = self.list.getSelectedItem()
		if controlID == 105:
			self.list = self.getControl(controlID)
			self.loadContentForAlbum( li )
		#start the slide show
		if controlID == 205:
			self.grid = self.getControl(controlID)
			#self.startSlideShowForAlbum( self.grid.getSelectedItem() )
			self.startSlideShowForAlbum( li )

	def delTree(self, target):
		try:
			shutil.rmtree(target)
		except:
			print "Could not delete plugin :" + target
			
	def copyFile(self,source,target):
		i= 0
		print "coia picture :" + source + " to " + target
		while i < 10:
			try:
				shutil.copy(source, target)
				i = 400
			except:
				print "Coulds not copy picture :" + source
				time.sleep(1)
				i = i + 1
		
	def startSlideShowForAlbum(self, li):
		path = li.getProperty("path")
		#w = PictureSlideShowWindow( "custom_ezee_slideshow.xml", __addonDir__)
		#w = PictureSlideShowWindow( "custom_ezee_slideshow.xml", __addonDir__, menuid = self.menuid, albumid=albumid )
		#w.doModal()
		#del w
	
		#self.preview = self.addControl(xbmcgui.ControlImage(742,216,1080,818, path))
		#self.addControl(xbmcgui.ControlImage(742,216,1080,818, item.get('thumbnail','')))

		xbmc.executebuiltin("ClearSlideshow")    
		albumid = li.getProperty("albumid")

		itemCount=0
		json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"PictureLibrary.GetPictures","id":1,"params": {"properties":["title","album","face","location","thumbnail"], "filter":{"albumid":'+str(albumid)+'}}}')
		json_query = unicode(json_query, 'utf-8', errors='ignore')
		jsonobject = simplejson.loads(json_query)
		if jsonobject['result'].has_key('pictures'):
			if os.path.exists(xbmc.translatePath("special://home/addons/"+__addonID__+"/pictures")):
				xbmc.log("delete : " + xbmc.translatePath("special://home/addons/"+__addonID__+"/pictures"))
				self.delTree(xbmc.translatePath("special://home/addons/"+__addonID__+"/pictures"))
			os.mkdir(xbmc.translatePath("special://home/addons/"+__addonID__+"/pictures"))
			
			print "Found pictures"
			for item in jsonobject['result']['pictures']:
				itemCount=itemCount+1
				print ("adding to slideshow: " + item.get('thumbnail',''))
				imagepath = "/Users/ashokjaiswal/Pictures/"+item.get('label','')
				self.copyFile(imagepath,xbmc.translatePath("special://home/addons/"+__addonID__+"/pictures"))
				xbmc.executebuiltin("AddToSlideshow(%s)" % item.get('thumbnail',''))

		print "# of pictures added to sideshow " + str(itemCount)
		xbmc.executebuiltin("SlideShow(special://home/addons/"+__addonID__+"/pictures, random)")
		#xbmc.executebuiltin( "SlideShow(/Users/ashokjaiswal/Pictures)" )

	def onAction( self, action ):
		print "onAction"
		print action
		if action in [ 9, 10, 117 ]:
			self.close()

def loadPictureAlbums(menuid):
    w = PicturesWindow( "custom_ezee_photos.xml", __addonDir__, menuid = menuid )
    w.doModal()
    del w

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
        
if ( __name__ == "__main__" ):
	print "============================="
	print __addonName__
	print __addonDir__
	print __addonID__
	print "============================="

	heading = __addonName__
	params = get_params()
	loadPictureAlbums( params["buttonid"] )