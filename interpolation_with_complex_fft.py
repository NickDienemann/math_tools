"""
This file contains the interpolation by directly using the complex amplitudes that result from the fft
"""
#imports
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt
import cmath
from numpy import random


def calculate_complex_amplitude_frequncy_pairs(y,sampling_rate):   
    """
    task: use fft to calculate the complex amplitudes together with their frequencies \n
    parameters: y(np.array()),sampling_rate(int(frequency of samples in Hz, e.g. how many samples are given within one second)) \n
    return value: complex_amplitude_frequency_pairs(zip(complex amplitude, corresponding frequency))
    """

    #sampling rate
    sr =  sampling_rate
    
    #fft
    Y = fft(y)
    N = len(Y)
    Y= Y/N
    n = np.arange(N)
    T = N/sr
    freq = n/T 

    #return the pairs 
    return zip(Y,freq)

def evaluate_function_at_x(complex_amplitude_frequency_pairs,x):
    """
    task: evaluate the function described by the complex_amplitude_frequency_pairs at value x \n
    parameters: complex_amplitude_frequency_pairs(zip(complex amplitude, corresponding frequency)),x(float at which function is evaluated) \n
    return value: float(y_value of function at value x)
    """
    
    summed_value=0
    for complex_amplitude,frequency in complex_amplitude_frequency_pairs:

        #use the real amplitudes to evaluate at current frequency
        summed_value+= complex_amplitude*cmath.exp(complex(0,2*np.pi*frequency*x))
 
    #discard the imaginary part manually(is insignificantly low ...e^-11)
    return summed_value.real

"""
#create the x and y values
x_aranged=np.arange(0,10,0.01)
y_aranged=[2*np.sin(3*2*np.pi*x)+np.sin(7*2*np.pi*x) for x in x_aranged]

#calculate the y_values according to fft  
values_by_fft=[evaluate_function_at_x(calculate_complex_amplitude_frequncy_pairs(y_aranged,100),x) for x in x_aranged]

#plot results
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x_aranged,values_by_fft,"r")
ax.plot(x_aranged,y_aranged,"b")

plt.show()

"""
#new plot
x_aranged_1=np.arange(0,10,1)
y_aranged=[pow(x,2)+random.randint(-2,2) for x in x_aranged_1]

pairs=[el for el in calculate_complex_amplitude_frequncy_pairs(y_aranged,1)]

x_aranged=np.arange(0,10,0.01)
values_by_fft=[evaluate_function_at_x(pairs,x) for x in x_aranged]

#plot results
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x_aranged,values_by_fft,"r")
ax.plot(x_aranged_1,y_aranged,".b")


plt.show()
