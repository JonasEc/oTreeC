from __future__ import division

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import os
import random as r			 
import numpy as np

try:
	from django.conf import settings
	ARIAL_TTF = os.path.join(settings.FONTS_DIR, "arial.ttf")
except ImportError:
	ARIAL_TTF = "arial.ttf"

from PIL import Image, ImageDraw, ImageFont, ImageChops

import io
import base64

import textwrap


author = 'Jonas Mueller-Gastell'

doc = """
This is the main part of the experiment.
"""

ARIAL = settings.FONTS_DIR


class Constants(BaseConstants):
### Randomness	
	seeder = os.urandom(4)
	r.seed(seeder)

### Base constants
	name_in_url = 'jonasmgstanfordExpermentC2'
	players_per_group = None
	num_rounds = 12
	failuretolerance = 8

### Money
	cost = c(3.5)
	hit = c(2.5)
	base = hit + cost	
	bonus = c(1)
	charitybonus = bonus
	basewithbonus = base + bonus
	basewithcost = base - cost

	max_charity_payment = c(10)
	multiplierhigh = 3
	multiplierlow = 0.5

### Picture Information
	totalneutral = 110
	majoritywords = 76
	minoritywords = 54
	totalwords = majoritywords + minoritywords + totalneutral

	textwidth = 110
	fontsize = 15

### WORD SPACE
	goodlist = ['play', 'good', 'pleasure', 'joy', 'reward', 'enjoy', 'fun', 'smile', 'laugh', 'felicity']
	badlist = ['bad', 'punishment', 'pain', 'toil', 'suffering', 'death', 'sickness', 'hatred', 'cry', 'loss']
	neutrallist =['shelf', 'tree', 'day', 'night', 'color', 'book', 'time', 'watch', 'shoe', 'tea']

### TIMER:
	timer = 90



class Subsession(BaseSubsession):

#### PAYOFF RANDOMISATION:
	def before_session_starts(self):
		for player in self.get_players():	
	### Picture good/ bad
			sample1 = player.participant.vars.get('treatmentalloc1')
			if self.round_number in sample1:
				player.quality = "Good"
				data1 = np.random.choice(Constants.goodlist, Constants.majoritywords)
				data1 = data1.tolist()
				data2 = np.random.choice(Constants.badlist, Constants.minoritywords)
				data2 = data2.tolist()
			else:
				player.quality = "Bad"
				data1 = np.random.choice(Constants.badlist, Constants.majoritywords)
				data1 = data1.tolist()
				data2 = np.random.choice(Constants.goodlist, Constants.minoritywords)
				data2 = data2.tolist()
			data3 = np.random.choice(Constants.neutrallist, Constants.totalneutral)
			data3 = data3.tolist()
			listbase = [data1, data2, data3]
			listbase = sum(listbase, [])
			data4 = np.random.choice(listbase,Constants.totalwords,replace = False)
			player.listoflists = " ".join(data4)

			player.expectation_randomiser = r.randint(0,100)
			player.expectation_randomiser_payoff = r.randint(0,100)

			sample2 = player.participant.vars.get('treatmentalloc2')
			if self.round_number in sample2:
				player.incentivefirst = True
			else:
				player.incentivefirst = False

			sample3 = player.participant.vars.get('treatmentalloc3')
			if self.round_number in sample3:
				player.high_incentive = True
			else:
				player.high_incentive = False


class Group(BaseGroup):
	pass


class Player(BasePlayer):

### Payoff Vars (INPUTS)
	bet = models.BooleanField()
	quality = models.CharField()
	incentivefirst = models.BooleanField()
	high_incentive = models.BooleanField()
	charityIncentive = models.CurrencyField()

	expectationvalue = models.FloatField(widget = widgets.SliderInput(attrs={'step': '1'}), min = 0, max = 100)
	expectation_randomiser = models.PositiveIntegerField()
	expectation_randomiser_payoff = models.PositiveIntegerField()

	charitypayoff = models.CurrencyField()
	min_charity_name = models.CharField()
	min_charity_value = models.CurrencyField()

### Payoff Vars (OUTPUTS)
	cumulative_payoff = models.CurrencyField()
	cumulative_payoff_charity = models.CurrencyField() 

### Other vars
	attentioncheck = models.CurrencyField(widget = widgets.RadioSelect)
	listoflists = models.TextField()


	def min_charity_finder(self):
		self.min_charity_name = self.participant.vars.get('min_charity_name')
		self.min_charity_value = self.participant.vars.get('min_charity_value')	
		return self.min_charity_value, self.min_charity_name

	def char_payoff_calc(self,incentive):
		if incentive == True:
			self.charityIncentive = c(Constants.multiplierhigh)/self.min_charity_value
		else:
			self.charityIncentive = c(Constants.multiplierlow)/self.min_charity_value
		if self.charityIncentive >=	Constants.max_charity_payment:
			self.charityIncentive = Constants.max_charity_payment
		return self.charityIncentive

	def worddictionarymaker(self):
		output = [[Constants.goodlist[k],Constants.badlist[k],Constants.neutrallist[k]] for k in range(0,len(Constants.badlist)) ]
		return output

	def picturemaker(self):	
		text = 	self.listoflists
		self.listoflists = ""

		#### CREATE THE DIMENSION OF THE PICTURE & the wrapper to be written
		# in console: myfont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
		font = ImageFont.truetype(ARIAL_TTF, Constants.fontsize)
		wrapper = textwrap.wrap(text, width=Constants.textwidth)
		lines = len(wrapper)
		width = 0
		height = 0
		for subwrap in wrapper:
			temp1, temp2 = font.getsize(subwrap)
			if temp1 > width:
				width = temp1
			if temp2 > height:
				height = temp2
		margin =  15
		offset = 15

		#### MAKE THE PICTURE
		image = Image.new("RGBA", (width + 2*margin, (height+3)*lines + 2*offset), (255,255,255))
		draw = ImageDraw.Draw(image)

		for line in wrapper:
			draw.text((margin, offset), line, font=font, fill = "#000000")
			offset += height + 3

		### SAVE THE PICTURE
		buff = io.BytesIO()
		buff.seek(0)
		image.save(buff, 'png')
		buff.seek(0)

		#### OUTPUT THE PICTURE
		encoded_image= base64.b64encode(buff.getvalue())
		return encoded_image


##### Calculate Payoff
	def set_payoffs(self):
		if self.participant.vars.get('picturenumber') == self.round_number:
			if self.player.participant.vars.get('charityquestions') == True:
				self.payoff = Constants.cost
				self.charitypayoff = c(0)
			elif self.participant.vars.get('bettingquestions') ==True:
				if self.bet == True:
					if self.quality == "Good":
						self.payoff = Constants.cost
						self.charitypayoff = self.charityIncentive
					else:
						self.payoff = c(0)
						self.charitypayoff = self.charityIncentive
				else:
					self.payoff = Constants.cost
					self.charitypayoff = c(0)
			else:
				self.charitypayoff = c(0)
				if self.expectationvalue >= self.expectation_randomiser:
					if self.quality == "Good":
						self.payoff = Constants.cost + Constants.bonus
						self.participant.vars['expeclucky'] = True
					else:
						self.payoff = Constants.cost
				else:
					if self.expectation_randomiser >= self.expectation_randomiser_payoff:
						self.payoff = Constants.cost + Constants.bonus
						self.participant.vars['expeclucky'] = True
					else:
						self.payoff = Constants.cost
		else:
			self.payoff = c(0)
			self.charitypayoff = c(0)		

		if self.participant.vars.get('expeclucky') != True:
			self.participant.vars['expeclucky'] = False
			
		return self.payoff, self.charitypayoff


	def cum_payoff(self):
		self.cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()]) 
		self.cumulative_payoff_charity = sum([p.charitypayoff for p in self.in_all_rounds()])
		self.participant.vars['bettingpartpayoff'] = self.cumulative_payoff
		self.participant.vars['bettingpartpayoff_charity'] = self.cumulative_payoff_charity



