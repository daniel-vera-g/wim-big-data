import os
import sys
import h5py

# EXAMPLE USAGE: python3 scripts/analyze-dataset.py millionSongSubset/A/I/O

# Get the current working directory
cwd = os.getcwd()

# Read first command line argument
path = sys.argv[1]

if not os.path.isdir(path):
    print("Path %s does not exist" % path)
    sys.exit(1)

os.chdir(cwd) # wechseln zu Ordner, in dem .h5-Dateien liegen
for file in os.listdir(path): # alle Dateien im Ordner
    print("\n---\nAnalyzing %s\n---\n" % file)

    full_path = os.path.join(path, file) 

    with h5py.File(full_path, 'r') as f: #File-Methode öffnet Dateien
        # Iterate over all keys programmatically and print them along with their values
        for key in f.keys():
            print(key)
            # Iterate over each value of the current key
            for value in f[key]:
                # if (key == "metadata"):
                #     print("\t", value, f[key][value][()]) 
                print("\t", value)
                if (value == "songs"):
                    print("\t\t", f[key][value][()])
