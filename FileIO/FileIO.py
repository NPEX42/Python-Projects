import os
import sys
from progress.spinner import Spinner
from progress.bar import Bar

files = []
# r=root, d=directories, f = files
count = 0;
spinner = Spinner("Locating...      ")
for r, d, f in os.walk("./"):
    for file in f:
        if '.java' in file:
            spinner.next();
            files.append(os.path.join(r, file))

spinner.finish();

bar = Bar("Saving To File... ",max=len(files));
fileList = open("Files.txt","w+");
for f in files:
    print("Found '"+str(f)+"'...")
    fileList.write(f)
    fileList.write("\n");
    bar.next();
fileList.close();
bar.finish();
