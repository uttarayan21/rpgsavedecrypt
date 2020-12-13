#!/usr/bin/env python3
import lzstring
import json
import argparse
import os
import errno
import sys

sys.tracebacklimit = 0


def decode_rpgsave(save):
    lz = lzstring.LZString()
    decoded = lz.decompressFromBase64(save)
    parsed = json.loads(decoded)
    decoded = json.dumps(parsed, indent=4, sort_keys=True)
    return decoded


def encode_rpgsave(save):
    lz = lzstring.LZString()
    encoded = lz.compressToBase64(save)
    return encoded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e",
                        "--encode",
                        help="Encode the decoded savefile",
                        action="store_true")
    parser.add_argument(
        "-o",
        "--output",
        help="Specify the output file instead of printing to stdout")
    parser.add_argument(
        "file", help="The rpgsave file which is either encoded / decoded")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    if os.path.isfile(args.file) == False:
        parser.print_usage()
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                args.file)
        sys.exit(1)
    else:
        f = open(args.file, "r")
    if args.encode == True:
        output = encode_rpgsave(f.read())
    else:
        output = decode_rpgsave(f.read())

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)


if __name__ == '__main__':
    main()
