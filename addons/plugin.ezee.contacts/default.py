
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

class ContactsWindow( xbmcgui.WindowXML ):
	def __init__(self, *args, **kwargs):
		self.heading = kwargs.get("heading") or ""
		self.menuid =  kwargs.get("menuid") or ""
	def onInit( self ):
		try:
			self.setFocus( self.getControl(int(self.menuid) ) )
		
			json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "ContactLibrary.GetContacts", "params": { "properties": [ "profilepic","name", "phone",  "email", "title", "thumbnail"], "sort": { "order": "ascending", "method": "album", "ignorearticle": true } }, "id": "libContacts"}')
			json_query = unicode(json_query, 'utf-8', errors='ignore')
			jsonobject = simplejson.loads(json_query)
			self.list = self.getControl(105)
			if jsonobject['result'].has_key('contacts'):
				ctr = 0
				for item in jsonobject['result']['contacts']:
					thumbnail = item.get('thumbnail','')
					if item.get('profilepic','') == 0 :
						thumbnail = "ezee/empty_profile_"+str(ctr%2)+".png"
					self.li = xbmcgui.ListItem(label=item.get('title',''), iconImage=thumbnail, thumbnailImage=thumbnail, path='')
					self.li.setProperty("contactid",str(item.get('contactid','')))
					self.li.setProperty("title",str(item.get('title','')))
					self.li.setProperty("profile_picture",thumbnail)
					self.li.setProperty("has_picture",str(item.get('profilepic','')))
					for phone in item['phone']:
						if phone.find("mobile") == 0 :
							self.li.setProperty("mobile",str(phone[phone.find(":")+1:]))
						if phone.find("work:") == 0 :
							self.li.setProperty("work",str(phone[phone.find(":")+1:]))
					for e in item['email']:
						email = str(e)
						self.li.setProperty("email",str(email[email.find(":"):]))
						
					self.list.addItem(self.li)
					ctr = ctr+1
				
			#self.loadContactFromListItem( self.list.getListItem(0) )
			
		except:
			print_exec()

	def loadContactFromListItem(self, li) :

		print "loadContactFromListItem"
		head = self.getControl(50)
		head.setLabel(li.getLabel())
		self.getControl(70).setLabel("Call "+li.getProperty("title"))
		self.getControl(74).setLabel(li.getProperty("mobile"))
		self.getControl(75).setLabel(li.getProperty("work"))
		self.getControl(76).setLabel(li.getProperty("email"))
		self.profile_image = self.getControl(60)
		self.profile_image.setImage(li.getProperty("profile_picture"))	
	
	def onFocus( self, controlID ):
		pass

	def onClick( self, controlID ):
		self.list = self.getControl(105)
		li = self.list.getSelectedItem()
		self.loadContactFromListItem( li )
		
	def onAction( self, action ):
		if action in [ 9, 10, 117 ]:
			self.close()

def loadContacts(menuid):
    w = ContactsWindow( "custom_ezee_contacts.xml", __addonDir__, menuid=menuid )
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
	heading = __addonName__
	params = get_params()
	loadContacts( params["buttonid"] )