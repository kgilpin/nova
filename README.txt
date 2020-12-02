
You need to change WebKit's ServletFactory.py if you use mod_rewrite to load the servlets.

				# Change needed so that file paths which are re-written to lowercase by mod_rewrite
				#   will stil work. Pretty sure this is a Windows-only problem
				theClass = None
				for key in module.__dict__.keys():
					if key.lower() == name:
						theClass = getattr(module, key)

				assert theClass, 'Cannot find expected servlet class named %s in %s.' % (repr(name), repr(path))

TODO:
Site looks ugly
There's no 'Abort' feature
Figure out some nice formatting for dates and times. Showing 1/100s of a second right now
Ensure that playerName and User.name are unique to their contexts
Field validation for required fields and data types ( integers )
Purchase*Events are similar, should have a common base class
Target star owner not get an event for SpyProbes
Can make probe jammers and nova shields cost different amounts than the probe and the nova bomb
Need to implement purchase events for nova shield and probe jammer
Are all Events invalid on dead stars?
Need to keep web users from being able to save the source code

RESOLVED:
Need to add some smart algorithms for building the initial boards
Need to add Production
Need to add the cron job for the game engine
Store the number of ships that a player has? It can be computed from garrisons and fleets
Need to test if DeathProbes render stars as grey
Not important : Need to have the login links on the action pages return the user to the action page, rather than the console


NOTES:

How to jump the web page to an anchor:

getAppletContext().showDocument
  (new URL("javascript:jumpTo(\"#JUMP\")"));
}
    
<SCRIPT>
function jumpTo(tag) {
   self.location=tag;
   }
</SCRIPT>
