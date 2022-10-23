# -*- coding: utf-8 -*-

""" Main entry point for the splat script """

import re
import argparse
import pandas as pd
from splat import __version__
from typing import NamedTuple, List, TextIO

class Args(NamedTuple):
    """ Command line arguments. """
    silac: TextIO
    tmt: List[TextIO]
    output: TextIO


def get_args() -> Args:
    """ Get command line arguments. """

    parser = argparse.ArgumentParser(
        description='SPLAT: Simultaneous Proteome Localization and Turnover',
        epilog='For more information, see GitHub repository at https://github.com/lau-lab/splat',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('silac', type=argparse.FileType('r'),
                        metavar='SILAC', help='SILAC input file')

    parser.add_argument('-t', '--tmt', type=argparse.FileType('r'), nargs='+',
                          metavar='TMT', help='TMT input file(s)')

    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='splat_output.txt')

    parser.add_argument('-v', '--version', action='version',
                        version=f'splat {__version__}')

    args = parser.parse_args()

    return Args(args.silac, args.tmt, args.output)


def main() -> None:
    """ Main entry point for the splat script """

    args = get_args()

    # Read in SILAC data
    silac_df = pd.read_csv(args.silac)
    silac_df = silac_df.rename(columns={'Unnamed: 0': 'concat',
                                        'k_deg': 'k',
                                        'R_squared': 'r2'})

    # Exit if no TMT data
    if not args.tmt:
        silac_df.to_csv(args.output, sep='\t', index=False)
        return None

    # Read in TMT data
    tmt_df = [pd.read_csv(tmt, sep='\t').assign(timepoint=re.sub('.*(time[0-9]+)_tmt.*$', '\\1', tmt.name)) for tmt in
              args.tmt]
    tmt_df = pd.concat(tmt_df)

    # Merge SILAC and TMT data
    def concat_peps(row):
        return row['sequence'] + '_' + str(row['charge'])

    tmt_df.insert(0, 'concat', tmt_df.apply(concat_peps, axis=1))
    tmt_df = tmt_df.merge(silac_df[['concat', 'k', 'r2', 'sd']], how='left')

    # Write output file
    tmt_df.to_csv(args.output, sep='\t')

    return None


if __name__ == '__main__':
    main()