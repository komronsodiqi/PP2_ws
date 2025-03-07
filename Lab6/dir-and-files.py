import os
import shutil

# 1. List dirs, files, and all items in a path
def lst(p):
    d = [i for i in os.listdir(p) if os.path.isdir(os.path.join(p, i))]
    f = [i for i in os.listdir(p) if os.path.isfile(os.path.join(p, i))]
    a = os.listdir(p)
    return d, f, a

# 2. Check path access
def chk(p):
    return {
        "ex": os.path.exists(p),
        "rd": os.access(p, os.R_OK),
        "wr": os.access(p, os.W_OK),
        "ex": os.access(p, os.X_OK)
    }

# 3. Path info
def pinfo(p):
    return {"fn": os.path.basename(p), "dr": os.path.dirname(p)} if os.path.exists(p) else "No path"

# 4. Count lines in a file
def cnt_ln(f):
    with open(f, 'r') as fl:
        return sum(1 for _ in fl)

# 5. Write list to file
def w_lst(lst, f):
    with open(f, 'w') as fl:
        fl.writelines('\n'.join(lst))

# 6. Create A-Z text files
def mk_txt():
    for i in range(65, 91):
        with open(f"{chr(i)}.txt", 'w') as fl:
            fl.write(f"This is {chr(i)}.txt\n")

# 7. Copy file
def cp(src, dst):
    shutil.copy(src, dst)

# 8. Delete file if exists and writable
def rm(f):
    if os.path.exists(f) and os.access(f, os.W_OK):
        os.remove(f)
        return "Deleted"
    return "No file / No access"


