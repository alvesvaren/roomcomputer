import sys
from . import hue_remote

if __name__ == "__main__":
    hue_remote.parseCommandline(sys.argv)
    hue_remote.end()