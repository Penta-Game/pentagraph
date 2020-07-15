from black import format_file_contents, FileMode, NothingChanged
from os import walk, path

if __name__ == "__main__":
    directory = path.join("pentagraph/")
    changes = [0, 0]

    for root, subdirs, files in walk(directory):
        for filename in files:
            file_path = path.join(root, filename)
            if file_path[-3:] != ".py":
                continue
            with open(file_path, "r") as f:
                try:
                    out = format_file_contents(
                        f.read(), fast=False, mode=FileMode()
                        )
                    changes[0] += 1
                    with open(file_path, "w") as f:
                        f.write(out)
                        print(f"{file_path} changed")
                except NothingChanged:
                    changes[1] += 1

    print(f"{changes[0]} changed/ {changes[1]} not changed")    
