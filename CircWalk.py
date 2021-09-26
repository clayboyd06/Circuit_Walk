import pickle
import os
import time
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
from pyltspice import * # poor error handling in the file 



## Setup maybe... maybe every time in runltSpice
netlist = netlist_fromfile(os.path.dirname('/Users/clayboyd/Desktop/Research/Printer/Circuits/dripdrop.asc')+'/dripdrop.net')
print(netlist)

params = {'V1': 100,
          'R1': 1,           
          'C1': 0.00001,
          'L1': 0.0002,
          'D1': '1N4148',       #D1, D2 fixed for now 
          'D2': '1N750',
          'R2': 10}

def run_ltspice(params):
    for key in params.keys():
        netchange(netlist, param(key, params[key]))
    data = runspice(netlist)
    I_d = data['I(D2)']
    time = data['time']
    print('Biggest current:', (max(I_d) - min(I_d)), 'A')
    return I_d, time

def error(trend):
    t = np.arange(0, 0.05, 1/5000)
    ideal_trend = 0.0214*np.sin(2*np.pi*3000*t)
    return ((I_d - ideal_trend)**2).mean()

#======================================================

I_d, time = run_ltspice(params)
plt.figure()
plt.xlim([0, 2.2e-3])
plt.plot(time.get_time_axis(0), I_d.get_wave(0))                 # Shows the time history of the probe
plt.show()

#IDEAL_CSV = 'idea_trend.csv'
#ideal_trend = pd.read_csv(IDEAL_CSV)  # TODO ideal_trend.csv <---- generate with module that creates csv from ac, dc, freq, count and 100 values




best_error = np.inf
timelimit = 60000

while time.time() < timelimit:
    new_params = evolve(params)  # TODO evolve()
    new_trend, x = run_ltspice(new_params)
    if error(new_trend) < best_error:
        params = new_params
        best_error = error(new_trend)


    
# EVOLVE: random evolutionary walk
def evolve():
    params[R1] = params[R1] + ((-1)**random.randint(1,2))*random.random()*params[R1]
    params[C1] = params[C1] + ((-1)**random.randint(1,2))*random.random()*params[C1]
    params[L1] = params[L1] + ((-1)**random.randint(1,2))*random.random()*params[L1]
    params[R2] = params[R2] + ((-1)**random.randint(1,2))*random.random()*params[R2]
           
#print('best model: ', params)
#print('best MSE: ', best_error)
print('done')
