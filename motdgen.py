import argparse
import os
import subprocess
import sys


def run_script(path):
    ret = subprocess.Popen(
        path, shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out


def run_scripts(path):
    output = ""
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.access(item_path, os.X_OK):
            output += run_script(item_path)
    return output


def generate_motd(source='/etc/motdgen.d/', outfile=None):
    message = run_scripts(source)
    if outfile:
        with open(outfile, 'w') as f:
            f.write(message)
    else:
        sys.stdout.write(message)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--source',
                        help='Directory containing scripts to generate MOTD',
                        dest='source',
                        default='/etc/motdgen.d/')
    parser.add_argument('-o',
                        '--output',
                        help='File to dump generated MOTD',
                        dest='dest',
                        default=None)
    args = parser.parse_args()
    generate_motd(args.source, args.dest)


if __name__ == '__main__':
    cli()
