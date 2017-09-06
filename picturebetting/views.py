from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


import io
import base64

from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG


class part2intro(Page):
	form_model = models.Player 
	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance	 and self.round_number == 1

class pictureIncentive(Page):
	form_model = models.Player 
	def is_displayed(self):
	 	return self.player.incentivefirst == True and self.player.participant.vars.get('failure') < Constants.failuretolerance
	def vars_for_template(self):
		self.player.min_charity_finder()
		self.player.char_payoff_calc(self.player.high_incentive)
		return {"mincharname": self.player.min_charity_name, "charpayoff": self.player.charityIncentive, "roundnumber": self.round_number}

class pictureAttention(Page):
	form_model = models.Player
	form_fields = ['attentioncheck']
	def attentioncheck_choices(self):
		if self.round_number % 3 == 0:
			return [c(Constants.multiplierhigh)/(2*self.player.min_charity_value),min(c(Constants.multiplierhigh)/self.player.min_charity_value, Constants.max_charity_payment), c(Constants.multiplierlow)/self.player.min_charity_value]			
		elif self.round_number % 3 == 1:
			return [min(c(Constants.multiplierhigh)/self.player.min_charity_value, Constants.max_charity_payment), c(Constants.multiplierlow)/self.player.min_charity_value,c(Constants.multiplierlow)/(0.65*self.player.min_charity_value)]			
		else:
			return [min(c(Constants.multiplierhigh)/self.player.min_charity_value, Constants.max_charity_payment), c(Constants.multiplierhigh)/(1.3*self.player.min_charity_value), c(Constants.multiplierlow)/self.player.min_charity_value]			
	def attentioncheck_error_message(self, value):
		if value != self.player.charityIncentive:
			return "Sorry that was wrong."
	def is_displayed(self):
	 	return self.player.incentivefirst == True and self.player.participant.vars.get('failure') < Constants.failuretolerance

class pictureInfoNew(Page):
	form_model = models.Player
	def vars_for_template(self):
		return {"png": self.player.picturemaker(), "roundnumber": self.round_number, "list_dictionary" : self.player.worddictionarymaker() }
	timeout_seconds = Constants.timer
	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance


class pictureBetting(Page):
	form_model = models.Player 
	form_fields = ['bet']
	def vars_for_template(self):
		self.player.min_charity_finder()
		self.player.char_payoff_calc(self.player.high_incentive)
		return {"mincharname": self.player.min_charity_name, "charpayoff": self.player.charityIncentive,"roundnumber": self.round_number}
	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance

class pictureExpecfinder(Page):
	form_model = models.Player 
	form_fields = ['expectationvalue']
	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance

class pictureIntermission(Page):
	def is_displayed(self):
		return self.round_number < Constants.num_rounds and self.player.participant.vars.get('failure') < Constants.failuretolerance
	def before_next_page(self):
		self.player.set_payoffs()
		if self.player.participant.vars.get('picturenumber') == self.round_number:
			if self.player.bet == True:
				self.player.participant.vars['betonpic'] = True
			else:
				self.player.participant.vars['betonpic'] = False
			if self.player.quality == 'Good':
				self.player.participant.vars['goodpic'] = True
			else:
				self.player.participant.vars['goodpic'] = False

class pictureIntEnd(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds and self.player.participant.vars.get('failure') < Constants.failuretolerance
	def before_next_page(self):
		self.player.set_payoffs()
		self.player.cum_payoff()
		##### SET THE PARTICIPANT VARS
		if self.player.participant.vars.get('picturenumber') == self.round_number :
			if self.player.bet == True:
				self.player.participant.vars['betonpic'] = True
			else:
				self.player.participant.vars['betonpic'] = False
			if self.player.quality == 'Good':
				self.player.participant.vars['goodpic'] = True
			else:
				self.player.participant.vars['goodpic'] = False
	

page_sequence = [
	part2intro,
	pictureIncentive,
	pictureAttention,
	pictureInfoNew,
	pictureExpecfinder,
	pictureBetting,
	pictureIntermission,
	pictureIntEnd,
]
