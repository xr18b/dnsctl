#!/usr/bin/python

'''
Importing requried libraries
'''
from os import symlink, path, listdir, readlink
from re import match
from sys import exit
import argparse

'''
Defining global variables
'''
G_dst_dir = "/code/resolv/" # Where the destination files are stored
G_resolv_path = "/etc/resolv.conf" # Where the 'resolv.conf' file is store on the system
G_resolv_isLink = path.islink(G_resolv_path) # Wether the 'resolv.conf' file is already a symlink
if G_resolv_isLink : G_init_dst = readlink(G_resolv_path) # If 'resolv.conf' is a link, the current destination

'''
This function will return a string containing the names of all available destination file
Note the file names will get trimmed from the '.resolv.conf' that they need to have at the end
'''
def get_available_dst():
    if path.exists(G_dst_dir) and path.isdir(G_dst_dir):
        T_files = listdir(G_dst_dir)
        T_dst = ""
        for this_file in T_files:
            if match('.*\.resolv\.conf', this_file):
                if len(T_dst) == 0:
                    T_dst += this_file.replace(".resolv.conf", "")
                else:
                    T_dst += " " + this_file.replace(".resolv.conf", "")

        if len(T_dst) == 0:
            exit("ERROR: No destination file available in '" + G_dst_dir + "'")

        return T_dst


def main() -> None:
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="Set DNS for the whole system, or query status of current DNS configuration.")

    parser.add_argument('-s', '--set',
                        required=False,
                        action="store_true",
                        default=False,
                        help="Set the DNS to a new scope (" + get_available_dst() + ")")

    parser.add_argument('-g', '--get',
                        required=False,
                        action="store_true",
                        default=False,
                        help="Get the name of the currently used profile")

    args = parser.parse_args()


if __name__ == "__main__":
    main()
