import sqlite3
from os.path import exists
import pandas as pd
import numpy as np


class PlatesDataset:
    DBFILE = 'dataset.sqlite'
    RNDSEED = 12345
    plates = None
    family_D = None
    family_L = None

    @classmethod
    def create_dataset(cls, seed=RNDSEED):
        cls.plates = pd.DataFrame(dtype=np.float64)
        rng = np.random.Generator(np.random.PCG64(seed))
        cls.plates['rand1'] = rng.uniform(0, 1, 10000)
        cls.plates['width'] = cls.plates['rand1'].apply(lambda x: 5 + 5 * x)
        cls.plates['rand1'] = rng.uniform(0, 1, 10000)
        cls.plates['length'] = cls.plates['rand1'].apply(lambda x: 15 + 15 * x)
        cls.plates['rand1'] = rng.uniform(0, 1, 10000)
        cls.plates['density'] = cls.plates['rand1'].apply(lambda x: 1 + 1 * x)
        cls.plates.drop(['rand1'], axis=1, inplace=True)
        bins = np.arange(15, 30+3, 3)
        labels = ["L{0}".format(i + 1) for i in range(len(bins) - 1)]
        cls.plates['catL'] = pd.cut(cls.plates['length'], bins=bins, labels=labels)
        bins = np.arange(1, 2+0.25, 0.25)
        labels = ["D{0}".format(i + 1) for i in range(len(bins) - 1)]
        cls.plates['catD'] = pd.cut(cls.plates['density'], bins=bins, labels=labels)
        cls.plates['surface'] = cls.plates['width'] * cls.plates['length']
        cls.plates['weight'] = cls.plates['surface'] * cls.plates['density']
        cls.family_L = cls.plates.groupby(['catL']).aggregate({'surface': ['min', 'max', 'mean', 'sum'],
                                                           'weight': ['min', 'max', 'mean', 'sum'],
                                                           'catL': 'count'}, axis="columns")
        cls.family_D = cls.plates.groupby(['catD']).aggregate({'surface': ['min', 'max', 'mean', 'sum'],
                                                           'weight': ['min', 'max', 'mean', 'sum'],
                                                           'catL': 'count'}, axis="columns")

    @classmethod
    def create_database(cls, file=DBFILE, force_create=False):
        if cls.plates is None:
            cls.create_dataset()
        if force_create or not exists(file):
            con = sqlite3.connect(file)
            cls.plates.to_sql('plates', con, if_exists='replace')
            cls.family_L.to_sql('family_L', con, if_exists='replace')
            cls.family_D.to_sql('family_D', con, if_exists='replace')
