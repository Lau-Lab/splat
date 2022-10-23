# -*- coding: utf-8 -*-

""" Main entry point for the splat script """

import os
import argparse
from splat import __version__
from typing import NamedTuple, List, TextIO


class Args(NamedTuple):
    """ Command line arguments. """
    input_silac: TextIO
    input_tmt: List[TextIO]
    output: TextIO
    version: bool


def get_args() -> Args:
    """ Get command line arguments. """

    parser = argparse.ArgumentParser(
        description='SPLAT: Simultaneous Proteome Localization and Turnover',
        epilog='For more information, see GitHub repository at https://github.com/lau-lab/splat',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_silac', type=argparse.FileType('r'),
                        metavar='SILAC', help='SILAC input file')

    parser.add_argument('input_tmt', type=argparse.FileType('r'), nargs='+',
                          metavar='TMT', help='TMT input file(s)')

    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='splat_output.txt')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()

    return Args(args.input_silac, args.input_tmt, args.output, args.version)


def main() -> None:

    args = get_args()

    print(args)

    return None


if __name__ == '__main__':
    main()