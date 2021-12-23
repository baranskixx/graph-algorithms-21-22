from os import system
import sys 
import glob






def get_main_part( f ):
#    print(f)
    file = open(f,"r")
    lines = file.readlines()
    code = []
    flag = False

    code = lines
    # modify the code here if you need (e.g., delete a common sorting procedure)
            
    f = f.replace("_"," ",1)
    x = f.find("_")
    if x == -1:
        return
    name = f[:x]
    name = name.replace(" ","_")+".py"
    print(name)
    out =  open( name, "w+" )
    for c in code:
        out.write(c)



directory = "*.py"
files = [f for f in glob.glob(directory, recursive=True) if not f.endswith("testy.py")]

print("rm RESULT")
for f in files:
    if f.find("_") >= 0:
      print("python",f," 2>>RESULT")
