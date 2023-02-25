from timeit import Timer
import platform

from plates_dataset import PlatesDataset


if __name__ == '__main__':
    print('Python', platform.python_version(), 'running on', platform.system(), platform.release(), f'({platform.machine()})')
    PlatesDataset.create_database(force_create=True)
    print(PlatesDataset.df.describe())
    print(PlatesDataset.df.memory_usage(deep=True))
    PlatesDataset.df.info(verbose=True)
    print()
