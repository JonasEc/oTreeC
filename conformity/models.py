from __future__ import division

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


from django.conf import settings

import os
import random	 
import numpy as np



from math import ceil

author = 'Jonas Mueller-Gastell'

doc = """
This is the main part of the experiment.
"""



class Constants(BaseConstants):
### Randomness	
	seeder = os.urandom(4)
	random.seed(seeder)

### Charities:
	charities = ["Amarillo","Austin","El Paso","Fort Worth","Houston","Irving","Lubbock","Midland","San Antonio","Tyler"] 

### Base constants
	name_in_url = 'Experiment'
	players_per_group = None
	num_rounds = len(charities)

### TREATMENT:
	# public = settings.SESSION_CONFIGS[0].get('public')
	# extraDonationTreat = settings.SESSION_CONFIGS[0].get('extraDonationTreat')
	# noFeedback = settings.SESSION_CONFIGS[0].get('noFeedback')
	# public = False
	# extraDonationTreat = True
	# noFeedback = False
	numberunderstandingquestions = 11
	accuracy = 1

### Money
	money = [c(3.72),c(5.72),c(6.72),c(7.67),c(8.57),c(9.42),c(10.22),c(10.97),c(11.67),c(12.32),c(12.92),c(13.47),c(13.97),c(14.42),c(14.82),c(15.17),c(15.47),c(15.72),c(15.92),c(16.07),c(16.17),c(16.26),c(16.34),c(16.41),c(16.47),c(16.52),c(16.56),c(16.59),c(16.61),c(16.62),c(16.62),c(16.63),c(16.63),c(16.63),c(16.64),c(16.64) ]
	showup = c(20)
	bonus = c(5)
	bonusForConfidence = 3
	confidenceBonus =c(bonusForConfidence)
	extraDonationNum = 5	
	extraDonation = c(extraDonationNum)

	r = np.linspace(1,bonusForConfidence,9)
	r2 = np.linspace(0,extraDonationNum,13)
	right_side_amounts = [c(0.05), c(0.10), c(0.25), c(0.50), c(0.75)] + [c(round(float(k),2)) for k in r]
	right_side_amounts_charity = list(reversed([c(float(k)) for k in r2]))


### TIMER:
	timerPractice = settings.SESSION_CONFIGS[0].get('practiceWaiting')




class Subsession(BaseSubsession):

#### PAYOFF RANDOMISATION:
	def creating_session(self):
		self.session.vars["NumberOfPlayers"] = len(self.get_players())
		selectedPlayer = random.randint(1,self.session.vars.get("NumberOfPlayers"))	
		self.session.vars["selectedPlayer"] = selectedPlayer

		self.session.vars["selectedRound"] = random.randint(1, Constants.num_rounds)

		selectedIncentive = random.randint(1,2)
		self.session.vars["selectedIncentive"] = selectedIncentive

		# for player in self.get_players():
		# 	selectedExtra = random.random()
		# 	if selectedExtra > 0.5:
		# 		player.participant.vars["DonateFirst"] = True
		# 		player.participant.vars["DonateSecond"] = False
		# 	else:
		# 		player.participant.vars["DonateFirst"] = False
		# 		player.participant.vars["DonateSecond"] = True



class Group(BaseGroup):
	pass
	#medianCommitment = models.PositiveIntegerField()





class Player(BasePlayer):
####### QUIZZ 
	truefalse0 = models.PositiveIntegerField(verbose_name="Question 1: How many of your waiting-time decisions, at most, will count for payment?")
	truefalse1 = models.PositiveIntegerField(verbose_name="Question 2: How many of your bonus-payment decisions, at most, will count for payment?")
	truefalse2 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name=("Question 3: Before you make your decisions in Rounds 2 through" + " " +str(Constants.num_rounds) +", will you know some information about the decisions made by others in the previous round?"))
	truefalse3 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name=("Question 4: Before making their decisions in Rounds 2 through" + " " +str(Constants.num_rounds) +", will others know your decision in particular in previous rounds?"))
	truefalse4 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name="Question 5: After all decisions are made, will others in this room learn your decision from the selected round?")
	truefalse5 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name="Question 6: After all decisions are made, will others in this room learn your decisions from the rounds that were not selected?")
	truefalse6 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'None of the above']],widget=widgets.RadioSelect(),verbose_name="Question 7: If you ARE the selected participant, your earnings for Make-A-Wish Foundation will depend on:")
	truefalse7 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'No additional time']],widget=widgets.RadioSelect(),verbose_name="Question 8: If you ARE the selected participant, you will have to wait:")
	truefalse8 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'None of the above']],widget=widgets.RadioSelect(),verbose_name="Question 9: If you ARE NOT the selected participant, your earnings for Make-A-Wish Foundation will depend on:")
	truefalse9 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'No additional time']],widget=widgets.RadioSelect(),verbose_name="Question 10: If you ARE NOT the selected participant, you will have to wait:")
	truefalse10 = models.PositiveIntegerField(verbose_name= "Question 11: Look at the decision table below. Please enter how much money (in whole dollars) the participant will be paid if the true median is 12 minutes and row number 5 is implemented by the computer and this question is chosen for payment.")
	truefalse11 = models.PositiveIntegerField(verbose_name= "Question 12: Look at the decision table below. Please enter how much money (in whole dollars) the participant will be paid if the true median is 16 minutes and row number 10 is implemented by the computer and this question is chosen for payment.")

######## ACTUAL DATA COLLECTED
	commitment = models.PositiveIntegerField(min=0,max=35)

	belief = models.PositiveIntegerField(min=0,max=35)

	confidence = models.CurrencyField()

	medianCommitment = models.PositiveIntegerField()
	timeMinutes = models.PositiveIntegerField()

	DonationDecision = models.CurrencyField()

	def calcmedian(self):
		commits = []
		for player in self.get_others_in_group():
			commits.append(player.commitment)
		commits = sorted(commits)
		self.medianCommitment = commits[ceil(self.session.vars.get("NumberOfPlayers")/2)-1]
		return self.medianCommitment

	def commitWait(self):
		roundN = str(self.session.vars.get("selectedRound")) 
		nameC = "commitment" + roundN 
		self.timeMinutes = self.participant.vars.get(nameC)
		return self.timeMinutes

######## Survey
	impactBelief   = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by what I THOUGHT other participants chose.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactKnow     = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by how much I KNEW other participants chose.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactLocation = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by the different locations of the Make-A-Wish Foundation across rounds.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactTexas    = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by the fact that the Make-A-Wish Foundation locations involved in this study were in Texas, as opposed to some other state in the U.S.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactFair     = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by what I thought was fair.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactNice     = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by what I thought was nice.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactGoodLook = models.PositiveIntegerField(verbose_name="My choices about my own waiting times were impacted by what I thought looked good to others.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	favMakeAWish   = models.PositiveIntegerField(verbose_name="I feel favorably about the Make-A-Wish Foundation." , choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())

	studentID = models.CharField(verbose_name="What is your Stanford Student ID Number?")
	sex = models.PositiveIntegerField(verbose_name="What is your sex?", choices=[[0,"Female"], [1,"Male"], [2, "Decline To State or Other"]], widget=widgets.RadioSelect())
	age = models.PositiveIntegerField(verbose_name="What is your age (in years)?", min=18,max=30)
	gradYear = models.PositiveIntegerField(verbose_name="In what year do you expect to graduate?", min=2018, max=2030)
	school = models.PositiveIntegerField(verbose_name="In what school is your degree program (or expected degree program)?", choices=[[1, "School of Business"],[2, "School of Eath Sciences"], [3,"School of Education"],[4, "School of Engineering"], [5,"School of Humanities & Sciences"], [6,"School of Law"], [7,"School of Medicine"], [8 ,"Unknown"]], widget=widgets.RadioSelect())
	econMajor= models.BooleanField(verbose_name="Are you an economics major?",choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect())
	GPA = models.FloatField(verbose_name="What is your GPA (on a 4.0 scale)?", min=0,max=4)

####### DATA FROM INTERNAL STUFF
	selectedPlayer = models.BooleanField()
	selectedRound = models.PositiveIntegerField()
	selectedIncentive = models.PositiveIntegerField()

	def makePartIntoField(self):
		self.selectedPlayer = self.session.vars["selectedPlayer"]
		self.selectedRound = self.session.vars["selectedRound"]
		self.selectedIncentive = self.session.vars["selectedIncentive"]

### SET PAYOFF
	def set_payoffs(self):
		roundN = str(self.session.vars.get("selectedRound")) 
		nameB = "belief" + roundN
		nameM = "median" + roundN
		nameC = "confidence" + roundN

		beliefOfSelectedRound = self.participant.vars.get(nameB)
		medianInSelectedRound = self.participant.vars.get(nameM)
		confidenceOfSelectedRound = self.participant.vars.get(nameC)

		selectedIncentive = self.session.vars.get("selectedIncentive")
		
		if selectedIncentive == 1:
			if beliefOfSelectedRound == medianInSelectedRound:
				bonus1 = Constants.bonus
			else:
				bonus1 = c(0)
			bonus2 = c(0)
		elif selectedIncentive == 2:
			randomVar = random.randint(0,len(Constants.right_side_amounts))
			if Constants.right_side_amounts[randomVar] <= confidenceOfSelectedRound:
				if  beliefOfSelectedRound in ([medianInSelectedRound] + [medianInSelectedRound - k for k in range(1,Constants.accuracy+1)] + [medianInSelectedRound + k for k in range(1,Constants.accuracy+1)]):
					bonus2 = Constants.confidenceBonus
				else:
					bonus2 = c(0)
			else:
				bonus2 = Constants.right_side_amounts[randomVar]
			bonus1 = c(0)

		if self.session.vars.get("extraDonationTreat"):
			randomRow = random.randint(0,len(Constants.right_side_amounts_charity)-1)
			if Constants.right_side_amounts_charity[randomRow] > self.participant.vars.get("DonationAmount"):
				bonus3 = Constants.right_side_amounts_charity[randomRow]
				self.participant.vars["outcomeCharityOwn"] = False
				self.charityDonation = c(0)

			else:
				self.participant.vars["charityDonation"] = Constants.extraDonation
				self.charityDonation = Constants.extraDonation
				bonus3 = c(0)
				self.participant.vars["outcomeCharityOwn"] = True
		else:
			bonus3 = c(0)

		self.payoff = Constants.showup + bonus1 + bonus2 + bonus3
		return self.payoff
