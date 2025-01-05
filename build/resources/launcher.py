import os

fp = os.path.dirname(__file__)
os.chdir(f"{fp}/../MacOS/")
os.system(f"open -a Terminal RoSniper")