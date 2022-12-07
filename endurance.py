import numpy as np
import matplotlib.pyplot as plt

cruise = 10000 #10kW at cruise
hover = 42000 #35kW to hover

battery = 6.66e3 #6.66kWh battery

cruise_time = np.linspace(0,60)
hover_time = 60/hover*(battery-cruise*cruise_time/60)

possible = hover_time>0
plt.plot(cruise_time[possible], hover_time[possible])
plt.xlabel("Cruise time at 55kts (minutes)")
plt.ylabel("Max power time (minutes)")
plt.show()
