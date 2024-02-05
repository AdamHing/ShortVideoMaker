import os

cwd = os.getcwd()
print(cwd)
print(os.path.abspath(os.path.join(cwd, os.pardir)))