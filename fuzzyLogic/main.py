import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

print(np.arange(0, 201, 1))

localization = ctrl.Antecedent(np.arange(0, 3, 1), 'localization')
number_of_rooms = ctrl.Antecedent(np.arange(0, 10, 1), 'number_of_rooms')
floor = ctrl.Antecedent(np.arange(0, 10, 1), 'floor')

price_per_square_meter = ctrl.Consequent(np.arange(3000, 20000, 100), 'price_per_square_meter')

localization.automf(3)
number_of_rooms.automf(5)
floor.automf(5)

price_per_square_meter['low'] = fuzz.trimf(price_per_square_meter.universe, [0, 0, 8000])
price_per_square_meter['medium'] = fuzz.trimf(price_per_square_meter.universe, [8000, 10000, 15000])
price_per_square_meter['high'] = fuzz.trimf(price_per_square_meter.universe, [15000, 20000, 20000])

price_per_square_meter.view()

rule1 = ctrl.Rule(localization['poor'] & floor['poor'] & number_of_rooms['poor'], price_per_square_meter['low'])
rule2 = ctrl.Rule(localization['poor'] & (floor['poor'] | floor['mediocre']), price_per_square_meter['low'])
rule3 = ctrl.Rule((localization['poor'] | floor['poor']) & (number_of_rooms['average'] | number_of_rooms['decent']), price_per_square_meter['low'])

rule4 = ctrl.Rule(localization['average'] & floor['average'] & number_of_rooms['average'], price_per_square_meter['medium'])
rule5 = ctrl.Rule(localization['average'] & floor['decent'] & number_of_rooms['decent'], price_per_square_meter['medium'])
rule6 = ctrl.Rule(localization['poor'] & floor['good'], price_per_square_meter['medium'])
rule7 = ctrl.Rule((localization['average'] | floor['decent']) & number_of_rooms['mediocre'], price_per_square_meter['medium'])
rule8 = ctrl.Rule(floor['good'] & (number_of_rooms['average'] | number_of_rooms['good']), price_per_square_meter['medium'])

rule9 = ctrl.Rule(localization['good'] & (floor['good'] | floor['decent']) & number_of_rooms['poor'], price_per_square_meter['high'])
rule10 = ctrl.Rule(localization['good'] & number_of_rooms['mediocre'], price_per_square_meter['high'])
rule11 = ctrl.Rule(floor['good'] & number_of_rooms['average'], price_per_square_meter['high'])


tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['localization'] = 0
tipping.input['floor'] = 1
tipping.input['number_of_rooms'] = 3

tipping.compute()
price_per_square_meter.view(sim=tipping)
print(tipping.output['price_per_square_meter'])

plt.show()




