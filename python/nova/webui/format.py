import re
from mx import DateTime

# Replace '<color>' with <font color="yellow"> and </color> with </font>
# Replace <unit qty=x /> with 'x ships'
# Replace <unit qty=1 /> with '1 ship'
# Replace <star name=Orion/> with an href link to the star in the applet
eventMessageReplacements = [ ( r'<color>', r'<font color="#FFFF00">') ,
							 ( r'</color>', r'</font>' ),
							 ( r'<unit qty=1\s*/>', r'1 ship'),
							 ( r'<unit qty=(\d+)\s*/>', r'\1 ships' ),
							 ( r'<star name=([^/]+)/>', r'''<a href="#applet" onclick="zoomToStar('\1')">\1</a>''' ) ]

def formatEventMessage(message):
	"""
	Formats the markup that is returned in the event message strings. See nova.Event#uiDescription
	"""
	for pattern, repl in eventMessageReplacements:
		message = re.sub(pattern, repl, message)
	return message

def formatValueForPage(value):
	"""
	This function plugs in to Python Server Pages
	See Webware-0.8/PSP/Docs/UsersGuide.html, 'formatter'
	"""
	if type(value) is DateTime.DateTimeType:
		return value.strftime('%Y-%m-%d %H:%M:%S')
	elif type(value) is DateTime.DateTimeDeltaType:
		result = ""
		if value > 0:
			if value.day == 1:
				result = "1 day, "
			elif value.day != 0:
				result = "%i days, " % value.day
			return result + "%.2i:%.2i:%.2i" % ( value.hour, value.minute, value.second )
		else:
			return "Now!"
	else:
		return str(value)