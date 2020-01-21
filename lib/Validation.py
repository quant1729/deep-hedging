import matplotlib as plt
import QuantLib as ql
import numpy as np
from Utilities import reshape_1D

class Validation:
	def __init__(self, model = None, data = None, N = None, process = None):
		self.model = model
		self.data = data
		self.process = process
		self.N = N
		
	def get_instrument(self, name = None, calculation_date = ql.Date.todaysDate(), **kwargs):
		if name is "European_Call":
			ql_payoff = ql.PlainVanillaPayoff(ql.Option.Call, kwargs["strike"])
			exercise_date = ql.EuropeanExercise(kwargs["maturity_date"])
			instrument = ql.VanillaOption(ql_payoff, exercise_date)

		if type(self.process).__name__ is "BlackScholesProcess":
			engine = ql.AnalyticEuropeanEngine(self.process.get_process(calculation_date))
			
		instrument.setPricingEngine(engine)
		return instrument
		
	def get_risk_neutral_PV(self, verbose = True):
		risk_neutral_price = -np.mean(self.data[-1])
		if verbose:
			print("The risk neutral price for the European call is {0}.".format(risk_neutral_price))
		return risk_neutral_price
		
	def get_model_PV(self, instrument=None):
		return instrument.NPV()

	def get_model_delta(self, instrument, s0 = None, calculation_date = None):
		process = self.process
		process.s0 = s0
			
		engine = ql.AnalyticEuropeanEngine(process.get_process(calculation_date))
		instrument.setPricingEngine(engine)

		return instrument.delta()
