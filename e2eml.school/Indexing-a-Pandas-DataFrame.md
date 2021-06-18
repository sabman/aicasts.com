"""
An example illustrating how to index pandas DataFrames.
"""
import numpy as np
import pandas as pd

mtns = pd.DataFrame([
    {'name': 'Mount Everest',
        'height (m)': 8848,
        'summited': 1953,
        'mountain range': 'Mahalangur Himalaya'},
    {'name': 'K2',
        'height (m)': 8611,
        'summited': 1954,
        'mountain range': 'Baltoro Karakoram'},
    {'name': 'Kangchenjunga',
        'height (m)': 8586,
        'summited': 1955,
        'mountain range': 'Kangchenjunga Himalaya'},
    {'name': 'Lhotse',
        'height (m)': 8516,
        'summited': 1956,
        'mountain range': 'Mahalangur Himalaya'},
])
mtns.set_index('name', inplace=True)

