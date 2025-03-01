from antoine import antoine
import numpy as np
import matplotlib.pyplot as plt

def raoult_law_kvalue( T, P, a, *gamma):
    # Calculates the equilibrium coefficient from Raoult's law
    # INPUTS:
    #
    #  T - temperature (units of K)
    #
    #  P - pressure (units of bar)
    #
    #  a - Antoine equation coefficients with coefficients for each species in
    #      a row. When drawing Antoine coefficients from NIST, these will expect T
    #      and p in units of K and bar. Antoine coefficients from other sources 
    #      will require compatible units.
    #
    #  gamma - OPTIONAL activity coefficients for use in a modified Raoult's law.
    #
    #  tempUnit - The units of temperature. Can be Kelvin, Fahrenheit, Celsius, or Rankine
    #             Parameter should be inputted as the first letter of the temperature scale.
    #             
    #
    # OUTPUT:
    #
    #  K - row vector containing the K-value for each species
    #
    #  Example: (eg: raoult_law_kvalue(500, 2, [1,2,3], *gamma))        
    #  
    # Code originally by James C. Sutherland
    # Modified by Tyler R. Josephson
    
    ns,nc = a.shape
    # makes np array of zeros 
    K = np.zeros(ns) 
    Ps = antoine(a, T)  
    K = Ps/P
    if gamma:
        K *= gamma
    return K
Methane= [4.35576, 1175.58, -2.071]
Water= [8.07, 1730.63,233.426]
T= 350 #K
P=1 #bar

a= np.array([Methane, Water])
for i, x in enumerate(x_methane):
    # Bubble point (start of condensation)
    T_bubble = T_initial  # initial guess for bubble point temperature
    for _ in range(100):  # Iterative solution
        K = raoult_law_kvalue(T_bubble, P, a)
        y = (K[0] * x) / (1 + x * (K[0] - 1))
        T_bubble -= 0.1 * (y - x) 

    bubble_temperatures[i] = T_bubble

    # Dew point (start of evaporation)
    T_dew = T_initial  # initial guess for dew point temperature
    for _ in range(100):  # Iterative solution
        K = raoult_law_kvalue(T_dew, P, a)
        y = (K[0] * x) / (1 + x * (K[0] - 1))
        T_dew += 0.1 * (y - x)

    dew_temperatures[i] = T_dew
    
#Z=P*v/(R*T*n)
plt.plot(x_methane, dew_temperatures, label="Dew Point", color="blue")
plt.plot(x_methane, bubble_temperatures, label="Bubble Point", color="red")
plt.fill_between(x_methane, bubble_temperatures, dew_temperatures, color='yellow', alpha=0.3, label="Two-Phase Region")
plt.xlabel("Mole Fraction of Methane")
plt.ylabel("Temperature (K)")
plt.title("Dew and Bubble Point Temperatures")
plt.legend()
plt.grid(True)
plt.show()

