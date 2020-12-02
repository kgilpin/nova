from NovaPage import NovaPage

class LogoutAction(NovaPage):
   def writeBody(self):
      self.response().delCookie('gameId')
      self.response().delCookie('userId')
      self.response().delCookie('playerId')
      self.response().delCookie('password')
      
      self.response().sendRedirect('/nova/')
