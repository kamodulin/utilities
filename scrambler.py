import os
import sys
import shutil
import filecmp
import time
import random
import string
import argparse

def duplicate(src, dest):
    os.mkdir(dest)
    files = os.listdir(src)
    for f in files:
        if os.path.isfile(os.path.join(src, f)):
            base, ext = os.path.splitext(f)
            if ext != ".log" and base[0] != ".":
                shutil.copy2(os.path.join(src, f), dest)

                #put filecmp integrity in here
    return dest

def integrity(orig, new):
    assert filecmp.cmp(orig, new), "File integrity compromised: {0}".format(new)

def randomize(name):
    extension = os.path.splitext(name)[1]
    random_name = ""

    for char in range(8):
        random_name += random.choice(string.ascii_letters+string.digits)
    return ("{0}{1}".format(random_name, extension))

def scramble(files):
    log = "scrambled.log"

    with open(log, "w") as writer:
        writer.write("scrambler.py log\n")
        writer.write("Created on {0}\n\n".format(time.ctime(os.path.getctime(log))))
        
        for old in files:
            new = randomize(old)
            writer.write("{0}  ->  {1}\n".format(old, new))
            os.rename(old, new)

def unscramble(files, log_dir):
    log = "{0}/scrambled.log".format(log_dir)

    with open(log, "r") as reader:
        content = reader.readlines()

    assert content[0] == "scrambler.py log\n", "Incorrect log format."

    for line in content[3:]:
        orig, new = line.strip('\n').split('  ->  ')
        os.rename(new, orig)

def main():
    parser = argparse.ArgumentParser(description="Scramble some files.")
    parser.add_argument("-d", "--directory", action="store", default=os.getcwd(), help="Path to root directory. Default is current directory.")
    parser.add_argument("-u", "--unscramble", action="store_true", help="Unscramble filenames.")
    args = parser.parse_args()

    root = args.directory
    s_dir = root + '/scrambled'
    u_dir = root + '/unscrambled'

    assert os.path.isdir(args.directory), "Not a directory."

    if not args.unscramble:
        assert not os.path.isdir(s_dir), "Scrambled directory already exists. Did you forget to add the -u flag?"

        s_dir = duplicate(root, s_dir)
        os.chdir(s_dir)
        
        for item in os.listdir(s_dir):
            integrity("{0}/{1}".format(root, item), item)
        
        scramble(os.listdir(os.getcwd()))
        
    else:
        assert os.path.isdir(s_dir), "Scrambled directory doesn't exist. Nothing to unscramble."
        assert not os.path.isdir(u_dir), "Unscrambled directory already exists."

        u_dir = duplicate(s_dir, u_dir)

        os.chdir(u_dir)
        unscramble(os.listdir(os.getcwd()), s_dir)

        for item in os.listdir(u_dir):
            integrity("{0}/{1}".format(root, item), item)

if __name__ == "__main__":
    main()