import pickle
f = open("data.pickle","rb")
data = pickle.load(f)
print(len(data['encodings']))
print(data["encodings"])
print(data["names"])