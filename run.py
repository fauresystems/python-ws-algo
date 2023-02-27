from timeit import Timer
import platform

from plates_dataset import PlatesDataset


def startup(force_create=False):
    PlatesDataset.create_database(force_create)
    print(PlatesDataset.plates.describe())
    print(PlatesDataset.plates.memory_usage(deep=True))
    PlatesDataset.plates.info(verbose=True)
    print(PlatesDataset.family_L.describe())
    print(PlatesDataset.family_L.memory_usage(deep=True))
    PlatesDataset.family_L.info(verbose=True)
    print(PlatesDataset.family_D.describe())
    print(PlatesDataset.family_D.memory_usage(deep=True))
    PlatesDataset.family_D.info(verbose=True)


if __name__ == '__main__':
    print('Python', platform.python_version(),
          'running on', platform.system(), platform.release(), f'({platform.machine()})')
    startup(force_create=False)
    # run and timeit algo SQL
    plates = PlatesDataset.load_input_dataframe()
    print()
    plates = PlatesDataset.load_input_objects()
    print()
