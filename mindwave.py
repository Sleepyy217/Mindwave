import wave
import numpy as np
import pandas as pd
import sys
import json
import time as time
from telnetlib import Telnet

# Initializing the arrays required to store the data.
attention_values = np.array([])
meditation_values = np.array([])
delta_values = np.array([])
theta_values = np.array([])
lowAlpha_values = np.array([])
highAlpha_values = np.array([])
lowBeta_values = np.array([])
highBeta_values = np.array([])
lowGamma_values = np.array([])
highGamma_values = np.array([])
blinkStrength_values = np.array([])
time_array = np.array([])

tn=Telnet('localhost',13854);

start= time.time();
print(start)
i=0;
tn.write(('{"enableRawOutput": true, "format": "Json"}').encode('ascii'));


outfile="null";
if len(sys.argv)>1:
	outfile=sys.argv[len(sys.argv)-1];
	outfptr=open(outfile,'w');

eSenseDict={'attention':0, 'meditation':0};
waveDict={'lowGamma':0, 'highGamma':0, 'highAlpha':0, 'delta':0, 'highBeta':0, 'lowAlpha':0, 'lowBeta':0, 'theta':0};
signalLevel=0;

end_time = start + 30;
while time.time() < end_time:
	blinkStrength=0;
	line=tn.read_until(('\r').encode('ascii'));
	if len(line) > 20:	
		timediff=time.time()-start;
		dict=json.loads(line);
		if "poorSignalLevel" in dict:
			signalLevel=dict['poorSignalLevel'];
		if "blinkStrength" in dict:
			blinkStrength=dict['blinkStrength'];
		if "eegPower" in dict:
			waveDict=dict['eegPower'];
			eSenseDict=dict['eSense'];
		
		
		time_array = np.append(time_array, timediff);
		#make sure the waveDict[WaveType] is before the value in the np.apppend function
		#see highGammaValues for example. 
		blinkStrength_values = np.append(blinkStrength_values, [blinkStrength]);
		lowGamma_values = np.append([waveDict['lowGamma']], lowGamma_values);
		highGamma_values = np.append([waveDict['highGamma']], highGamma_values);
		highAlpha_values = np.append([waveDict['highAlpha']],highAlpha_values);
		delta_values = np.append( [waveDict['delta']], delta_values);
		lowBeta_values = np.append([waveDict['lowBeta']],lowBeta_values);
		highBeta_values = np.append( [waveDict['highBeta']], highBeta_values);
		theta_values = np.append([waveDict['theta']], theta_values);
		lowAlpha_values = np.append([waveDict['lowAlpha']], lowAlpha_values);
		
		#print the output of the last reading onto the console. 
		outputstr=f"Elapsed Time: {time_array[-1]}  loGamma: {waveDict['lowGamma'][-1]} hiGamma: {waveDict['highGamma'][-1]} hiAlpha: {waveDict['highAlpha'][-1]} Delta:{waveDict['delta'][-1]} hiBeta: {waveDict['highBeta'][-1]} loAlpha:{waveDict['lowAlpha'][-1]} loBeta:{waveDict['lowBeta'][-1]} theta:{waveDict['theta'][-1]}"
		print (outputstr);
		
		
person_name = input('Enter the name of the person: ')
times_to_invalidate = input('What timestamps should not be recorded? ->')



from numpy import nan as Nan
import pandas as pd 

#create the exported csv file
dataset = pd.DataFrame()
dataset['time'] = time_array

for attr,array  in waveDict.items():
	dataset[attr] = array;

dataset.to_csv('data_eeg.csv')      
    
tn.close();
#outfptr.close();