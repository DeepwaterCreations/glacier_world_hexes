#!/usr/bin/env python3
import random

hex_source_file = "needed"
hex_dest_files = ["gou", "iron", "elizibet"]

if __name__ == "__main__":

    with open(hex_source_file, mode='r+') as hex_source:
        needed_hexes = hex_source.readlines()
        if len(needed_hexes) == 0:
            print("All hexes accounted for!")
            sys.exit(0)

        new_hex = random.choice(needed_hexes)
        needed_hexes.remove(new_hex)
        print(new_hex)
        hex_source.truncate(0)
        hex_source.writelines(needed_hexes)

