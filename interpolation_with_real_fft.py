"""
This file contains the interpolation via transfomration of the fft amplitudes into its real parts for sine and cosine
"""


#imports
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt
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
    Y = Y/(2*N)
    n = np.arange(N)
    T = N/sr
    freq = n/T 

    #return the pairs 
    return zip(Y,freq)

def convert_complex_amplitude(complex_amp):
    """
    task: convert the given complex amplitude into the corresponding real amplitudes a_n(used for cosine part) and b_n(used for sine part) \n
    parameters: complex_amp(numpy.complex) \n
    return value:
    """

    a_n=2*complex_amp.real
    b_n=-2*complex_amp.imag
    return a_n,b_n 

def evaluate_function_at_x(complex_amplitude_frequency_pairs,x):
    """
    task: evaluate the function described by the complex_amplitude_frequency_pairs at value x \n
    parameters: complex_amplitude_frequency_pairs(zip(complex amplitude, corresponding frequency)),x(float at which function is evaluated) \n
    return value: float(y_value of function at value x)
    """

    summed_value=0
    for complex_amplitude,frequency in complex_amplitude_frequency_pairs:

        #get real and imaginary part of the amplitude
        a_n,b_n= convert_complex_amplitude(complex_amplitude)

        #use the real amplitudes to evaluate at current frequency
        summed_value+= a_n*np.cos(2*np.pi*frequency*x)+b_n* np.sin(2*np.pi*frequency*x)
 
    return summed_value


#create the x and y values
x_aranged=np.arange(0,10,0.1)
#y_aranged=[3*np.sin(2*np.pi*x)+2 for x in x_aranged]
y_aranged=[pow(x,2)+random.randint(-2,10) for x in x_aranged]

#calculate the y_values according to fft  
values_by_fft=[evaluate_function_at_x(calculate_complex_amplitude_frequncy_pairs(y_aranged,10),x) for x in x_aranged]

#plot results
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x_aranged,values_by_fft,"r")
ax.plot(x_aranged,y_aranged,".b")

plt.show()

