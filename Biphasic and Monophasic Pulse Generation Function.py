# -*- coding: utf-8 -*-
"""V5 Pulse Generation Code (Synchronization) GitHub.ipynb"""

##################### Biphasic Pulse ###########################

import numpy as np
import math as math
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

np.set_printoptions(threshold=np.inf,suppress=True,linewidth=100000,precision=10)

def Biphasic_generation_function(block_frequency,pulse_width,simulation_time,Amplitude):

  def time_stamps_function():

    frequency_train = 0.5
    period_train = 1 / frequency_train          # 2 s

    block_time = 1.5                            # ON time
    period_block = 1 / block_frequency          # e.g. 20 ms

    total_pulses_block = int(round(block_time / period_block))

    print('Period of Train:', period_train, 's')
    print('Period of Block:', period_block, 's')
    print('Simulation Time:', simulation_time)
    print('Pulses per block:', total_pulses_block)
    print()

    total_train = []

    block_starts = []

    block_start = 0.0

    while block_start < simulation_time:

        block_starts.append(block_start)

        for pulse in range(total_pulses_block):

            pulse_start = block_start + pulse * period_block

            # Don't generate pulses beyond the simulation
            if pulse_start + 2*pulse_width > simulation_time:
                break

            total_train.extend([
                pulse_start,
                pulse_start,
                pulse_start + pulse_width,
                pulse_start + pulse_width,
                pulse_start + 2*pulse_width,
                pulse_start + 2*pulse_width
            ])

        block_start += period_train

    total_train = np.array(total_train)

    total_time_stamps = len(total_train)

    print("Block starts:")
    print(block_starts[:10], "...")

    print("Spacing between blocks:")
    print(np.diff(block_starts)[:10], "...")

    return total_train, total_time_stamps, block_start

  def pulse_stamps_function(pulse_model,total_time_stamps):
    pulse_total = np.array([])
    pulse_count = 0

    while pulse_count < total_time_stamps:   # expected number of amplitude entries

      pulse_total = np.concatenate((pulse_total, pulse_model), axis=None)
      pulse_count += pulse_model.size

    #Amplitude modification
    pulse_total = pulse_total * Amplitude
    pulse_total = pulse_total.astype(int)

    pulse_format_zero = np.array([0])
    pulse_total = np.concatenate((pulse_format_zero,pulse_total), axis=None)


    return pulse_total,pulse_count


  def train_format():

    def initial_and_final_train(total_train):
      #Note: Sim4Life requires a start with a 0.0s time-stamp. Otherwise it sends error message.
      #Any simulation time-step can work.
      #Train addition helps to normalize the last value of the array, so it ends at a pulse of 0.

      initial_time = 20 #seconds
      total_train = total_train + initial_time

      train_format_zero = np.array([0])
      total_train = np.concatenate((train_format_zero,total_train), axis=None)

      return total_train

    def pair_generator(): #testing_tool
      lista_a0 = g.tolist()
      lista_a = [float(f"{x:.5f}") for x in lista_a0]
      lista_c = pulse_total.tolist()
      lista = list(zip(lista_a,lista_c))

      #print("len(time): ",len(lista_a))
      #print("len(pulse): ",len(lista_c))
      #print("Mismatch: ",len(lista_a) - len(lista_c))
      #print('\n')
      print("Pair-wise Match: ", lista)

    g = initial_and_final_train(total_train)

    fig, ax2 = plt.subplots(figsize=(20, 8))
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax2.set_yticks([]) # Removes major ticks
    ax2.yaxis.set_minor_locator(plt.NullLocator()) # Removes minor
    #ax2.set_xlim(34.455,34.465)
    #ax2.set_xlim(20,60)
    #ax2.set_xlim(20,30)
    #ax2.set_xlim(20,20.50)
    #ax2.set_xlim(20,160)
    ax2.set_xlim(0,160)
    #ax2.set_xlim(19.999,20.001)
    ax2.plot(g,pulse_total)
    #plt.show()
    time = np.array_str(g)
    pulse = np.array_str(pulse_total)
    print("time: " + time.replace('\n','').replace('[','').replace(']',''))
    print("pulse: " + pulse.replace('\n','').replace('[','').replace(']',''))
    time_final = time.replace('\n','').replace('[','').replace(']','')
    pulse_final = pulse.replace('\n','').replace('[','').replace(']','')
    with open(f"BXiphasic_Pulses_Frequency_({block_frequency}_Hz).txt", "w") as text_file:
      text_file.write(f'{time_final}' + "\n" + f'{pulse_final}')
    #print('\n')

    pair_generator()
    return g

  total_train,total_time_stamps,time_passed = time_stamps_function()
  pulse_model_bi = np.array([0,1,1,-1,-1,0])
  pulse_models = [pulse_model_bi]

  for i in pulse_models:
    pulse_total,pulse_count = pulse_stamps_function(i,total_time_stamps)
    g = train_format()
    #print('\n')
    #print('Last 10 values: ')
    #print(total_train[-10:])
    #print(pulse_total[-10:])
  return g, pulse_total

def Monophasic_generation_function(frequency_train,pulse_width,simulation_time):

  def time_stamps_function():

    period_train = 1/frequency_train
    t1=  -0.25
    t2= t1+pulse_width
    initial_train = np.array([t1,t1,t2,t2])
    total_repetitions = int(simulation_time/period_train)
    repeated_times = 1
    total_train = initial_train

    #print(period_train,simulation_time,total_repetitions)

    while repeated_times < total_repetitions: #expected total

      next_train = np.array([
          total_train[-4] + period_train,
          total_train[-4] + period_train,
          total_train[-4] + period_train + pulse_width,
          total_train[-4] + period_train + pulse_width
          ])

      total_train = np.concatenate((total_train, next_train), axis=None)
      repeated_times += 1

    total_time_stamps = np.count_nonzero(total_train != 0) + np.count_nonzero(total_train == 0)

    #synchronizes monophasic and biphasic together
    total_train = total_train[4:]
      #[4:] is an arbitrarily chosen start based on 0.5Hz, any other frequency will keep displaying negative starting values.
    next_train = np.array([
    total_train[-4] + period_train,
    total_train[-4] + period_train,
    total_train[-4] + period_train + pulse_width,
    total_train[-4] + period_train + pulse_width])
    total_train = np.concatenate((total_train, next_train), axis=None)

    init_a = np.array([0])
    total_train = np.concatenate((init_a, total_train), axis=None)

    return total_train, total_time_stamps

  def pulse_stamps_function(pulse_model):

    pulse_total = np.array([])
    pulse_count = 0

    while pulse_count < b:   # expected number of amplitude entries

      pulse_total = np.concatenate((pulse_total, pulse_model), axis=None)
      pulse_count += pulse_model.size

    init_c = np.array([0])
    pulse_total = np.concatenate((init_c, pulse_total), axis=None)

    return pulse_total,pulse_count

  def train_format():

    list_a0 = a.tolist()
    list_a = [float(f"{x:.5f}") for x in list_a0] #Time_list
    list_c = c.tolist()                           #Pulse Amplitude List
    list_zip = list(zip(list_a,list_c))

    fig, ax1 = plt.subplots(figsize=(20, 8))
    ax1.set_yticks([]) # Removes major ticks
    ax1.yaxis.set_minor_locator(plt.NullLocator()) # Removes minor
    #ax1.set_xlim(20,60)
    ax1.set_xlim(20,160)
    ax1.plot(a,c,color='red')
    plt.show()
    time = np.array_str(a)
    pulse = np.array_str(c)
    print("time: " + time.replace('\n','').replace('[','').replace(']',''))
    print("pulse: " + pulse.replace('\n','').replace('[','').replace(']',''))
    time_final = time.replace('\n','').replace('[','').replace(']','')
    pulse_final = pulse.replace('\n','').replace('[','').replace(']','')
    with open(f"Monophasic_Pulses_Frequency_({frequency_train}_Hz).txt", "w") as text_file:
      text_file.write(f'{time_final}' + "\n" + f'{pulse_final}')

    print("len(time):",len(list_a))
    print("len(pulse):",len(list_c))
    print("Mismatch: ",len(list_a) - len(list_c))
    print('\n')
    print("Pair-wise Match: ", list_zip)

    return list_a,list_c

  a,b = time_stamps_function()
  pulse_model_mono = np.array([0,1,1,0])
  pulse_models = [pulse_model_mono]

  for i in pulse_models:
    c,d = pulse_stamps_function(i)
    a, c = train_format()
    print('\n')
  return a, c

##################### Monophasic Pulse ###########################

#(#Frequency [Hz],#Width [s], #Simulation [s])

g, pulse_total = Biphasic_generation_function(5,0.0002,160,1)
a, c = Monophasic_generation_function(0.5,0.0002,180)

fig, ax = plt.subplots(figsize=(20,8))

ax.plot(g, pulse_total, color='green', label='E-Stim 2')
ax.plot(a, c, color='blue', label='E-Stim 1')

ax.set_xlim(0,160)
ax.set_yticks([])
ax.legend()

plt.show()

print(a[1::4][:10])
