import os
PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
SOURCE_PATH = os.path.join(PROJECT_ROOT_PATH, 'app', 'src', 'main')
TEST_PATH = os.path.join(PROJECT_ROOT_PATH, 'app', 'src', 'test')
DATA_PATH = os.path.join(PROJECT_ROOT_PATH, 'data')
GEN_PATH = os.path.join(PROJECT_ROOT_PATH, 'generated')

# print(PROJECT_ROOT_PATH, SOURCE_PATH, TEST_PATH, DATA_PATH, GEN_PATH, sep='\n')