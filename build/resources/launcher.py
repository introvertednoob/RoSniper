import os

fp = __file__.replace(os.path.basename(__file__), "")
os.chdir(f"{fp}/../MacOS/")
os.system(f"open -a Terminal RoSniper")