import sqlite3
from os.path import exists
import pandas as pd
import numpy as np


class PlatesDataset:
    DBFILE = 'dataset.sqlite'
    RNDSEED = 12345
    df = None

    @classmethod
    def create_dataset(cls, seed=RNDSEED):
        cls.df = pd.DataFrame(dtype=np.float64)
        rng = np.random.Generator(np.random.PCG64(seed))
        cls.df['rand1'] = rng.uniform(0, 1, 10000)
        cls.df['width'] = cls.df['rand1'].apply(lambda x: 5 + 5 * x)
        cls.df['rand1'] = rng.uniform(0, 1, 10000)
        cls.df['length'] = cls.df['rand1'].apply(lambda x: 15 + 15 * x)
        cls.df['rand1'] = rng.uniform(0, 1, 10000)
        cls.df['density'] = cls.df['rand1'].apply(lambda x: 1 + 1 * x)
        cls.df.drop(['rand1'], axis=1, inplace=True)
        bins = np.arange(15, 30+3, 3)
        labels = ["L{0}".format(i + 1) for i in range(len(bins) - 1)]
        cls.df['catL'] = pd.cut(cls.df['length'], bins=bins, labels=labels)
        bins = np.arange(1, 2+0.25, 0.25)
        labels = ["D{0}".format(i + 1) for i in range(len(bins) - 1)]
        cls.df['catD'] = pd.cut(cls.df['density'], bins=bins, labels=labels)
        cls.df['surface'] = cls.df['width'] * cls.df['length']
        cls.df['weight'] = cls.df['surface'] * cls.df['density']

    @classmethod
    def create_database(cls, file=DBFILE, force_create=False):
        if cls.df is None:
            cls.create_dataset()
        if force_create or not exists(file):
            con = sqlite3.connect(file)
            cls.df.to_sql('plates', con, if_exists='replace')
