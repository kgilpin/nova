from nova.BattleEvent import BattleEvent
from nova.trigger.trigger import Message, Trigger, TRIGGER_TYPE_MESSAGE

class BattleMessageTrigger(Trigger):
	"""
	Sends a message to a player whenever he fights a battle
	"""
	
	def triggerType(self): 
		return TRIGGER_TYPE_MESSAGE
	
	def applyTo(self, event, player): 
		if not isinstance(event, BattleEvent):
			return 0
		return event.attacker() is player or event.defender() is player

	def message(self, event, player):
		if event.victor() is player:
			outcome = 'won at <star name=%s/> against' % event.star().name()
		else:
			outcome = 'lost at <star name=%s/> to' % event.star().name()
		if event.attacker() is player:
			opponent = event.defender()
		else:
			opponent = event.attacker()
		subject = 'You %s %s' % ( outcome, opponent.name() )
		return Message(subject, event.uiDescription(player))
