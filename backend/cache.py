# Fetching data is expensive
# So let's not do it often
# Using pickle to serialize and deserialze data

import pickle
import os

data_path = "cache/"

def get_cache(funcname):
    cache_file = os.path.join(data_path, f"{funcname}.txt")
    is_cached = os.path.exists(cache_file)
    if not is_cached: return None
    with open(cache_file, 'rb') as f:  # open a text file
        data_loaded = pickle.load(f) # deserialize using load()
        return data_loaded

def put_cache(funcname, data):
    cache_file = os.path.join(data_path, f"{funcname}.txt")  # Use os.path.join for cross-platform path construction
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
        f.close()
    
