import pickle
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

class Parse:
        def __init__(self):
                pass


# with open ('resume_parsing_model.pkl', 'rb') as f:
#     parsing = pickle.load(f)

with open('./resume_parsing_model.pkl', 'rb') as f:
        model = pickle.load(f)
        


print(model)
# model.predict()

