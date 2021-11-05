'''
Estimation of price per square meter of the apartment

Authors: Martyna Klebba, Klaudia Pardo

Requirements:
pip install scikit-fuzzy
pip install numpy
'''
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#input
localization = ctrl.Antecedent(np.arange(0, 5, 1), 'localization')
number_of_rooms = ctrl.Antecedent(np.arange(0, 11, 1), 'number_of_rooms')
floor = ctrl.Antecedent(np.arange(0, 11, 1), 'floor')

#output
price_per_square_meter = ctrl.Consequent(np.arange(3000, 20000, 1), 'price_per_square_meter')

# Auto-membership function
localization.automf(3)
number_of_rooms.automf(3)
floor.automf(3)

# Custom membership functions
price_per_square_meter['low'] = fuzz.trimf(price_per_square_meter.universe, [3000, 3000, 10000])
price_per_square_meter['medium'] = fuzz.trimf(price_per_square_meter.universe, [3000, 10000, 20000])
price_per_square_meter['high'] = fuzz.trimf(price_per_square_meter.universe, [10000, 20000, 20000])

'''localization.view()
number_of_rooms.view()
floor.view()
price_per_square_meter.view()'''

#fuzzy relationship between input and output variables.
rule1 = ctrl.Rule(antecedent=((floor['poor'] & localization['poor'] & number_of_rooms['average']) |
                              (floor['poor'] & localization['poor']) |
                              (floor['average'] & localization['poor'] & number_of_rooms['poor']) |
                              floor['poor'] & localization['poor'] & number_of_rooms['good']),
                  consequent=price_per_square_meter['low'])

rule2 = ctrl.Rule(antecedent=((floor['good'] & localization['poor'] & number_of_rooms['poor']) |
                              (floor['poor'] & localization['poor'] & number_of_rooms['good']) |
                              (floor['poor'] & localization['average']) |
                              (floor['good'] & localization['poor'] & number_of_rooms['good']) |
                              (floor['average'] & localization['average'] & number_of_rooms['average']) |
                              (floor['poor'] & localization['good'] & number_of_rooms['poor'])),
                  consequent=price_per_square_meter['medium'])

rule3 = ctrl.Rule(antecedent=((number_of_rooms['good'] & localization['good'] & floor['good']) |
                              (number_of_rooms['poor'] & localization['good'] & floor['good']) |
                              (number_of_rooms['average'] & localization['good'] & floor['average']) |
                              (number_of_rooms['good'] & localization['good']) |
                              (number_of_rooms['average'] & localization['good'] & floor['good'])),
                  consequent=price_per_square_meter['high'])

meter_pricing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
meter_pricing = ctrl.ControlSystemSimulation(meter_pricing_ctrl)

## Pass inputs using Antecedent labels
meter_pricing.input['localization'] = 0
meter_pricing.input['floor'] = 1
meter_pricing.input['number_of_rooms'] = 5

meter_pricing.compute()
price_per_square_meter.view(sim=meter_pricing)
print(meter_pricing.output['price_per_square_meter'])




