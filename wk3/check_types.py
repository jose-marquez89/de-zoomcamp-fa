import os 
import pandas as pd

# iterate through files

def get_directory(color: str) -> dict:
    dir_path = f"data/{color}"
    fnames = os.listdir(dir_path)
    type_directory = {}
    
    for f in fnames:
        df = pd.read_parquet(os.path.join(dir_path, f))

        for c in df.columns:
            cur_dtype = df[c].dtype
            if c in type_directory:
                type_directory[c].append(cur_dtype)
            else:
                type_directory[c] = [cur_dtype]

    return type_directory

def check_types(directory: dict) -> None:
    for col, types in directory.items():
        curtype = None
        for t in types:
            if curtype is None:
                curtype = t
            else:
                if t != curtype:
                    print(f"Column [{col}] contains inconsistent datatypes")
                    print(f"\t{t} vs {curtype}")
                    break

if __name__ == "__main__":
    d = get_directory("green")
    check_types(d)


# save only a zip of the columns and their data types
# compare to the next dataset's datatypes
# record any columns that differ from everything else