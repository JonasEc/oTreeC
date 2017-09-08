from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


### INTRO PAGES

class welcome(Page):
	def is_displayed(self):
		return self.round_number == 1

class IRB(Page):
	def is_displayed(self):
		return self.round_number == 1

class instructions(Page):
	def is_displayed(self):
		return self.round_number == 1

class quizz(Page):
	def is_displayed(self):
		return self.round_number == 1

	form_model = models.Player
	def get_form_fields(self):
		fields_to_show=[]
		for key in range(1,Constants.numberunderstandingquestions+1):
			fields_to_show.append('truefalse{}'.format(key))
		return fields_to_show
	def error_message(self, values):
		summand = 0
		if values["truefalse1"] != 1:
			summand += 1
		if values["truefalse2"] != Constants.feedback:
			summand += 1
		if values["truefalse3"] != False:
			summand += 1
		if values["truefalse4"] != Constants.public:
			summand += 1
		if values["truefalse5"] != False:
			summand += 1	
		if values["truefalse6"] != 0:
			summand += 1	
		if values["truefalse7"] != 0:
			summand += 1	
		if values["truefalse8"] != 2:
			summand += 1	
		if values["truefalse9"] != 2:
			summand += 1	
		if summand > 1:	
			return 'Sorry, you got ' + str(summand) + " questions wrong."
			summand = 0
		elif summand == 1:
			summand = 0
			return 'Almost there! You just got one question wrong!'

class practice(Page):
	def is_displayed(self):
		return self.round_number == 1	
	timeout_seconds = Constants.timerPractice
	timer_text = "Time left to wait:"

#### MAIN PAGES

class commit(Page):
	form_model = models.Player 
	form_fields = ['commitment', 'belief']
	def vars_for_template(self):
		return {"charity": Constants.charities[self.round_number-1], "listCommits1": Constants.money[0:12], "listCommits2": Constants.money[12:24], "listCommits3": Constants.money[24:36]}
	def before_next_page(self):
		nameC = "commitment" + str(self.round_number)
		nameB = "belief" + str(self.round_number)
		self.player.participant.vars[nameC] = self.player.commitment
		self.player.participant.vars[nameB] = self.player.belief

class feedback(Page):
	def is_displayed(self):
		return Constants.feedback and self.round_number < Constants.num_rounds
	def vars_for_template(self):
		return {"median": self.player.calcmedian(),  "one": 1, "money": Constants.money[self.player.calcmedian()-1], "charity":Constants.charities[self.round_number-1]}

class feedbackLast(Page):
	def is_displayed(self):
		return Constants.feedback and self.round_number == Constants.num_rounds
	def vars_for_template(self):
		return {"median": self.player.calcmedian(), "one": 1, "money": Constants.money[self.player.calcmedian()-1], "charity":Constants.charities[self.round_number-1]}


class waiting(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds and self.player.id_in_group == self.session.vars.get("selectedPlayer")

	timer_text = "Time left to wait:"	
	def get_timeout_seconds(self):	
		return self.player.participant.vars.get("committedMinutes")*60

	def vars_for_template(self):
		return {"committed": self.player.participant.vars.get("committedMinutes")*60,"committedMin": self.player.participant.vars.get("committedMinutes"), "money": Constants.money[self.player.timeMinutes -1],"round": self.session.vars.get("selectedRound"), "charity":Constants.charities[self.session.vars.get("selectedRound")-1] }


class notwaiting(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds and self.player.id_in_group != self.session.vars.get("selectedPlayer")


##### SURVEY PAGES

class survey1(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	form_model = models.Player
	form_fields = ['impactBelief', 'impactKnow', 'impactLocation', 'impactTexas', 'impactFair', 'impactNice', 'impactGoodLook','favMakeAWish']


class survey2(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	form_model = models.Player
	form_fields = ['studentID', 'sex', 'age', 'gradYear', 'school', 'econMajor', 'GPA']

	def before_next_page(self):
		self.player.set_payoffs()

class payment(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds
	def vars_for_template(self):
		if self.player.payoff > Constants.showup:
			extra = True
		else:
			extra = False
		if self.session.vars.get("selectedPlayer") == self.player.id_in_group:
			waiting = True
		else:
			waiting = False
		return {"payment": self.player.payoff, "extra": extra, "waiting": waiting, "round": self.session.vars.get("selectedRound"), "charity": Constants.charities[self.session.vars.get("selectedRound")-1], "money": Constants.money[self.player.timeMinutes -1]} 	



##### WAIT PAGES
 
class quizzWaitPage(WaitPage):
	def is_displayed(self):
		return self.round_number == 1

class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		for player in self.group.get_players():
			player.medianCommitment = player.calcmedian()
			nameM = "median" +str(self.round_number)
			player.participant.vars[nameM] = player.medianCommitment
			if self.round_number == Constants.num_rounds:
				player.timeMinutes = player.commitWait()
				player.participant.vars["committedMinutes"] = player.commitWait()

page_sequence = [
	welcome,
	IRB,
	instructions,
	quizz,
	quizzWaitPage,
	practice,
	commit,
	ResultsWaitPage,
	feedback,
	feedbackLast,
	waiting,
	notwaiting,
	survey1,
	survey2,
	payment
]
