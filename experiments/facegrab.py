"""
The MIT License (MIT)

Copyright (c) 2014 Ankit Aggarwal <ankitaggarwal011@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function
import sys
import os
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
from datetime import datetime
from random import randint

def create_dir(prefix):
    dir_c = os.path.join(os.getcwd(), prefix, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    try:
        os.makedirs(dir_c)
    except OSError as e:
        if e.errno != 17:
            pass
        else:
            print("Cannot create a folder.")
            exit
    return dir_c

def genUrl(name):
    return "http://graph.facebook.com/picture?id=" + name + "&width=800"

def getProfile(photoUrl, saveUrl):
    print("Downloading " + photoUrl + ".")
    response = urlopen(photoUrl)
    if response.geturl() != "https://static.xx.fbcdn.net/rsrc.php/v3/yo/r/UlIqmHJn-SK.gif":
        open(saveUrl, "wb").write(response.read())
        return True
    return False

def getImages(sizeDataset):
    id = randint(1, int(1e4))
    photoCount = 0
    folder = create_dir("facegrab")
    while photoCount < sizeDataset:
        if getProfile(genUrl(str(id)), folder + "/" + str(id) + ".jpg"):
            photoCount += 1
            id += 1
        else:
            id += 10
    print("\nFace Dataset created in facegrab folder.")
    print("Size: " + str(photoCount))
    return

def main():
    arguments = list(sys.argv[1:])
    if len(arguments) == 1 and arguments[0].isdigit() and int(arguments[0]) < int(1e7):
        getImages(int(arguments[0]))
    else:
        print("\nIncorrect arguments.")
        print("Usage: python facegrab.py <dataset size (integer < 10,000,000)>")
    return

if __name__ == "__main__":
    main()
