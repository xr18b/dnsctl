#!/usr/bin/env python3

'''
Importing requried libraries
'''
from os import symlink, path, readlink, remove
from sys import exit
import argparse
import glob

'''
Defining global variables
'''
G_dst_dir = "/code/resolv/" # Where the destination files are stored
G_resolv_path = "/etc/resolv.conf" # Where the 'resolv.conf' file is store on the system
G_resolv_isLink = path.islink(G_resolv_path) # Wether the 'resolv.conf' file is already a symlink
if G_resolv_isLink : G_init_dst = readlink(G_resolv_path) # If 'resolv.conf' is a link, the current destination


def get_available_dst() -> str:
    '''
    Return a string containing the names of all available destination file
    Note the file names will get trimmed of the '.resolv.conf' that they need to have at the end
    '''
    if not path.exists(G_dst_dir) or not path.isdir(G_dst_dir):
        exit(f"ERROR: Directory '{G_dst_dir}' does not exist")

    _glob_files = glob.glob(path.join(G_dst_dir, '*.resolv.conf'))
    if len(_glob_files) < 1:
        exit(f"ERROR: No destination file available in '{G_dst_dir}'")
    return ' '.join([path.basename(file).removesuffix('.resolv.conf') for file in _glob_files])


def set_destination(new_dest: str):
    """
    Change the '/etc/resolv.conf' link to a new destination
    """
    target = G_dst_dir + new_dest + ".resolv.conf"
    if path.exists(target):

        try:
            remove(G_resolv_path)
        except PermissionError as error:
            exit("ERROR: you are not allowed to change DNS")
        except Exception as error:
            print("Error while deleting the old link")
            exit(error)
            
        try:
            symlink(target, G_resolv_path)
        except PermissionError as error:
            exit("ERROR: you are not allowed to change DNS")
        except Exception as error:
            exit(error)

        exit()
    else:
        exit("ERROR: '" + target + ".resolv.conf' does not exist")


def get_destination():
    """
    Print the current destination of '/etc/resolv.conf'
    """
    print("DNS is set to: " + G_init_dst.replace(G_dst_dir, "").replace(".resolv.conf", ""))
    exit()


def main() -> None:
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="Set DNS for the whole system, or query status of current DNS configuration.")

    parser.add_argument('-s', '--set',
                        required=False,
                        metavar="SCOPE",
                        help="Set the DNS to a new scope (" + get_available_dst() + ")")

    parser.add_argument('-g', '--get',
                        required=False,
                        action="store_true",
                        default=False,
                        help="Get the name of the currently used profile")

    args = parser.parse_args()

    if not G_resolv_isLink:
        print("ERROR: '" + G_resolv_path + "' is not a symlink")
        exit()

    if args.get:
        get_destination()

    if args.set:
        set_destination(new_dest=args.set)

    parser.print_help()


if __name__ == "__main__":
    main()
