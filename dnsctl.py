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
        raise NotADirectoryError('Directory \'{}\' does not exist!'.format(G_dst_dir))

    _glob_files = glob.glob(path.join(G_dst_dir, '*.resolv.conf'))
    if len(_glob_files) < 1:
        raise FileNotFoundError('No destination file available in \'{}\' does not exist!'.format(G_dst_dir))

    return ' '.join([path.basename(file).removesuffix('.resolv.conf') for file in _glob_files])

def set_destination(new_dest: str):
    """
    Change the '/etc/resolv.conf' link to a new destination
    """
    _target = G_dst_dir + new_dest + ".resolv.conf"
    if path.exists(_target):
        remove(G_resolv_path)
        symlink(_target, G_resolv_path)
    else:
        raise FileNotFoundError('Destination not found: \'{}\''.format(_target))


def get_destination():
    """
    Print the current destination of '/etc/resolv.conf'
    """
    _cur_dst = G_init_dst.replace(G_dst_dir, "").replace(".resolv.conf", "")
    print(f"DNS is set to: {_cur_dst}")


def main() -> None:

    try:
        L_available_dst = get_available_dst()
    except NotADirectoryError as error:
        exit(f"ERROR: Directory '{G_dst_dir}' does not exists")
    except FileNotFoundError as error:
        exit(f"ERROR: No destination file available in '{G_dst_dir}'")
    except Exception as error:
        exit(f"ERROR: {error}")

    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="Set DNS for the whole system, or query status of current DNS configuration.")

    parser.add_argument('-s', '--set',
                        required=False,
                        metavar="SCOPE",
                        help="Set the DNS to a new scope (" + L_available_dst + ")")

    parser.add_argument('-g', '--get',
                        required=False,
                        action="store_true",
                        default=False,
                        help="Get the name of the currently used profile")

    args = parser.parse_args()

    if args.get:
        if not G_resolv_isLink:
            exit(f"ERROR: '{G_resolv_path}' is not a symlink")

        get_destination()
        return

    if args.set:
        if not G_resolv_isLink:
            exit(f"ERROR: '{G_resolv_path}' is not a symlink")

        try:
            set_destination(new_dest=args.set)
        except PermissionError as error:
            exit(f"ERROR: You are not allowed to change DNS")
        except FileNotFoundError as error:
            exit(f"ERROR: Destination \'{args.set}\' does not exists")
        except Exception as error:
            exit(f"ERROR: {error}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()

