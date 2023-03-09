from inspect import indentsize
from textwrap import indent
import pandas as pd
import numpy as np
import sys

raw_csv_file = sys.argv[-1]
dataset = pd.read_csv(raw_csv_file)
print(dataset.info())
print(f'the length of the input is {len(dataset)} entries')

target_columns = ['Valence', 'Arousal', 'Dominance']
for tc in target_columns:
    dataset[tc] = [ -1 for i in dataset.iterrows()]

baseline_duration = int(input('how long was the calibration period?'))

for ind, row in dataset.iterrows():
    if row.time < baseline_duration:
        for tc in target_columns:
            dataset.at[ind, tc] = 0

num_of_clips = int(input('how many clips were played?'))
clip_start = baseline_duration
for i in range(num_of_clips):
    emotions = [0,0,0]
    for x, tc in enumerate(target_columns):
        emotions[x] = int(input(f'what was the reported {tc} response for the {i+1}th clip?'))

    clip_end = int(input(f'when did the {i+1}th clip end?'))


    print(clip_start, clip_end)
    for ind, row in dataset.iterrows(): 
        if row.time > clip_start and row.time < clip_end:
            for j, tc in enumerate(target_columns):
                dataset.at[ind, tc] = emotions[j]

    if i+2 <= num_of_clips:
        clip_start = int(input(f'when did the {i+2}th clip start?'))

rows_to_drop = []
for ind, row in dataset.iterrows():
    if row.Valence == -1:
        rows_to_drop.append(ind)

dataset.drop(rows_to_drop, axis=0, inplace=True)
print(dataset.info())
outfile = input('What file name would you like to export these changes to? ')
dataset.to_csv(outfile)




