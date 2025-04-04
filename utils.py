import pandas as pd
import numpy as np


def get_data():
    patients = pd.read_csv('IndividualDetails.csv')
    total = patients.shape[0]
    active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
    recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
    death = patients[patients['current_status'] == 'Deceased'].shape[0]
    return patients, total, active, recovered, death
