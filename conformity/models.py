from __future__ import division

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

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
	charities = ["Amarillo","Austin"]#,"El Paso","Fort Worth","Houston","Irving","Lubbock","Midland","San Antonio","Tyler"] 

### Base constants
	name_in_url = 'Experiment'
	players_per_group = 2
	num_rounds = len(charities)

### TREATMENT:
	public = False
	feedback = True
	numberunderstandingquestions = 11
	accuracy = 1

### Money
	money = [c(3.72),c(5.72),c(6.72),c(7.67),c(8.57),c(9.42),c(10.22),c(10.97),c(11.67),c(12.32),c(12.92),c(13.47),c(13.97),c(14.42),c(14.82),c(15.17),c(15.47),c(15.72),c(15.92),c(16.07),c(16.17),c(16.26),c(16.34),c(16.41),c(16.47),c(16.52),c(16.56),c(16.59),c(16.61),c(16.62),c(16.62),c(16.63),c(16.63),c(16.63),c(16.64),c(16.64) ]
	showup = c(20)
	bonus = c(5)
	bonusForConfidence = 3
	confidenceBonus =c(bonusForConfidence)

	r = np.linspace(1,bonusForConfidence,9)
	right_side_amounts = [c(0.05), c(0.10), c(0.25), c(0.50), c(0.75)] + [c(float(k)) for k in r]

### TIMER:
	timerPractice = 15




class Subsession(BaseSubsession):

#### PAYOFF RANDOMISATION:
	def before_session_starts(self):
		selectedPlayer = random.randint(1,Constants.players_per_group)	
		self.session.vars["selectedPlayer"] = selectedPlayer

		self.session.vars["selectedRound"] = random.randint(1, Constants.num_rounds)

		selectedIncentive = random.randint(1,2)
		self.session.vars["selectedIncentive"] = selectedIncentive


class Group(BaseGroup):
	pass
	#medianCommitment = models.PositiveIntegerField()





class Player(BasePlayer):
####### QUIZZ 
	truefalse1 = models.PositiveIntegerField(verbose_name="How many of your decisions, at most, will count for payment?")
	truefalse2 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name=("Before you make your decisions in Rounds 2 through" + " " +str(Constants.num_rounds) +", will you know some information about the decisions made in the previous round?"))
	truefalse3 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name=("Before making their decisions in Rounds 2 through" + " " +str(Constants.num_rounds) +", will others know your decision in particular in previous rounds?"))
	truefalse4 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name="After all decisions are made, will others in this room learn your decision from the selected round?")
	truefalse5 = models.BooleanField(choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect(),verbose_name="After all decisions are made, will others in this room learn your decisions from the rounds that were not selected?")
	truefalse6 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'None of the above']],widget=widgets.RadioSelect(),verbose_name="If you ARE the selected participant, your earnings for Make-A-Wish Foundation will depend on:")
	truefalse7 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'No additional time']],widget=widgets.RadioSelect(),verbose_name="If you ARE the selected participant, you will have to wait:")
	truefalse8 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'None of the above']],widget=widgets.RadioSelect(),verbose_name="If you ARE NOT the selected participant, your earnings for Make-A-Wish Foundation will depend on:")
	truefalse9 = models.PositiveIntegerField(choices=[[0, 'The amount of time you chose to stay in the selected round.'],[1, 'The amount of time others chose to stay in the selected round'],[2, 'No additional time']],widget=widgets.RadioSelect(),verbose_name="If you ARE NOT the selected participant, you will have to wait:")
	truefalse10 = models.PositiveIntegerField(verbose_name= "Look at the decision table below. Please enter how much money (in whole dollars) the participant will be paid if the true median is 12 minutes and row number 5 is implemented by the computer and this question is chosen for payment.")
	truefalse11 = models.PositiveIntegerField(verbose_name= "Look at the decision table below. Please enter how much money (in whole dollars) the participant will be paid if the true median is 16 minutes and row number 10 is implemented by the computer and this question is chosen for payment.")

######## ACTUAL DATA COLLECTED
	commitment = models.PositiveIntegerField(min=0,max=35)

	belief = models.PositiveIntegerField(min=0,max=35)

	confidence = models.CurrencyField()

	medianCommitment = models.PositiveIntegerField()
	timeMinutes = models.PositiveIntegerField()

	def calcmedian(self):
		commits = []
		for player in self.get_others_in_group():
			commits.append(player.commitment)
		commits = sorted(commits)
		self.medianCommitment = commits[ceil(Constants.players_per_group/2)-1]
		return self.medianCommitment

	def commitWait(self):
		roundN = str(self.session.vars.get("selectedRound")) 
		nameC = "commitment" + roundN 
		self.timeMinutes = self.participant.vars.get(nameC)
		return self.timeMinutes

######## Survey
	impactBelief   = models.PositiveIntegerField(verbose_name="My choices were impacted by what I THOUGHT other participants chose.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactKnow     = models.PositiveIntegerField(verbose_name="My choices were impacted by how much I KNEW other participants chose.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactLocation = models.PositiveIntegerField(verbose_name="My choices were impacted by the different locations of the Make-A-Wish Foundation across rounds.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactTexas    = models.PositiveIntegerField(verbose_name="My choices were impacted by the fact that the Make-A-Wish Foundation locations involved in this study were in Texas, as opposed to some other state in the U.S.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactFair     = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought was fair.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactNice     = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought was nice.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactGoodLook = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought looked good to others.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	favMakeAWish   = models.PositiveIntegerField(verbose_name="I feel favorably about the Make-A-Wish Foundation." , choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())

	studentID = models.CharField(verbose_name="What is your Stanford Student ID Number?")
	sex = models.PositiveIntegerField(verbose_name="What is your sex?", choices=[[0,"Female"], [1,"Male"], [2, "Decline To State or Other"]], widget=widgets.RadioSelect())
	age = models.PositiveIntegerField(verbose_name="What is your age (in years)?", min=18,max=30)
	gradYear = models.PositiveIntegerField(verbose_name="In what year do you expect to graduate?", min=2018, max=2030)
	school = models.PositiveIntegerField(verbose_name="In what school is your degree program (or expected degree program)?", choices=[[1, "School of Business"],[2, "School of Eath Sciences"], [3,"School of Education"],[4, "School of Engineering"], [5,"School of Humanities & Sciences"], [6,"School of Law"], [7,"School of Medicine"], [8 ,"Unknown"]], widget=widgets.RadioSelect())
	econMajor= models.BooleanField(verbose_name="Are you an economics major?",choices=[[1, 'Yes'],[0, 'No']],widget=widgets.RadioSelect())
	GPA = models.FloatField(verbose_name="What is your GPA (on a 4.0 scale)?", min=0,max=4)



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
		self.payoff = Constants.showup + bonus1 + bonus2
		return self.payoff




