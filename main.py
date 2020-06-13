#!/usr/bin/env python3
import random
import sys

if __name__ == "__main__":

    try:
        source_file = sys.argv[1]
        dest_file = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <hex list file> <player name>") 

    with open(source_file, mode='r+') as hex_source: 
        needed_hexes = hex_source.readlines()
        if len(needed_hexes) == 0:
            print("All hexes accounted for!")
            sys.exit(0)

        new_hex = random.choice(needed_hexes)
        needed_hexes.remove(new_hex)
        print(new_hex)
        hex_source.truncate(0)
        hex_source.writelines(needed_hexes)

