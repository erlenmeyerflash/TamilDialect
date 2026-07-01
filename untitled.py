import os

folder_two_levels_up = os.path.dirname(os.path.dirname(__file__))

print(folder_two_levels_up)  # myapp