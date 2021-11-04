import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


#wejścia
localization = ctrl.Antecedent(np.arange(0, 5, 1), 'localization')
number_of_rooms = ctrl.Antecedent(np.arange(0, 11, 1), 'number_of_rooms')
floor = ctrl.Antecedent(np.arange(0, 11, 1), 'floor')

#wyjście
price_per_square_meter = ctrl.Consequent(np.arange(3000, 20001, 1), 'price_per_square_meter')


localization.automf(3)
number_of_rooms.automf(3)
floor.automf(3)

price_per_square_meter['low'] = fuzz.trimf(price_per_square_meter.universe, [3000, 3000, 10000])
price_per_square_meter['medium'] = fuzz.trimf(price_per_square_meter.universe, [3000, 3000, 20000])
price_per_square_meter['high'] = fuzz.trimf(price_per_square_meter.universe, [10000, 20000, 20000])

price_per_square_meter.view()

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

rule3 = ctrl.Rule(antecedent=((floor['good'] & localization['good'] & number_of_rooms['good']) |
                              (floor['poor'] & localization['good'] & number_of_rooms['good']) |
                              (floor['average'] & localization['good'] & number_of_rooms['average']) |
                              (floor['good'] & localization['good']) |
                              (floor['average'] & localization['good'] & number_of_rooms['good'])),
                  consequent=price_per_square_meter['high'])

rule2.view()

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['localization'] = 2
tipping.input['floor'] = 4
tipping.input['number_of_rooms'] = 7

tipping.compute()
price_per_square_meter.view(sim=tipping)
print(tipping.output['price_per_square_meter'])

plt.show()




