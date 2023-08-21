#!/usr/bin/env python3

import argparse
from collections import defaultdict

def parse_gff(gff_file, feature_type):
    bins = defaultdict(int)

    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue

            fields = line.strip().split('\t')
            if len(fields) < 3:
                continue

            contig = fields[0]
            feature = fields[2]

            if feature == feature_type:
                start = int(fields[3])
                end = int(fields[4])

                bin_start = (start // bin_size) * bin_size
                bin_end = bin_start + bin_size

                bin_key = f"{contig}:{bin_start}-{bin_end}"
                bins[bin_key] += 1

    return bins

def main():
    parser = argparse.ArgumentParser(description="Count features within bins in a GFF file")
    parser.add_argument("-i", "--input", help="Input GFF file", required=True)
    parser.add_argument("-f", "--feature", help="Feature type to count", required=True)
    parser.add_argument("-b", "--bin_size", type=int, help="Size of each bin in base pairs", required=True)
    args = parser.parse_args()

    global bin_size
    bin_size = args.bin_size

    bins = parse_gff(args.input, args.feature)

    for bin_key, count in bins.items():
        print(f"{bin_key}\t{args.feature}\t{count}")

if __name__ == "__main__":
    main()



# ./Gen-Bin_featurecount.py -i <gff> -f <feature_type> -b 200000 > output.txt



