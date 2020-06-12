import pandas as pd
import numpy as np


def find_cosponsor_of_my_party(senator):
    if senator['party'] == 'D':
        return senator['cosponsors_D']
    if senator['party'] == 'R':
        return senator['cosponsors_R']
    if senator['party'] == 'I':
        return senator['cosponsors_ID']

def calc_cosponsor_party_percent(df, party_code):
    if df['cosponsors_{}'.format(party_code)] > 0:
        return round(df['cosponsors_{}'.format(party_code)] / (df['cosponsors_D'] + \
                                                          df['cosponsors_R'] + \
                                                          df['cosponsors_ID']), 3)
    else:
        return 0.0