import argparse

def process_gff_file(input_file, feature_type, bin_size, output_file, remove_feat):
    bins = {}

    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue

            columns = line.strip().split('\t')
            contig = columns[0]
            feat_type = columns[2]
            start = int(columns[3])
            end = int(columns[4])

            if feat_type == feature_type:
                bin_start = (start // bin_size) * bin_size
                bin_end = bin_start + bin_size

                if (contig, bin_start, bin_end) not in bins:
                    bins[(contig, bin_start, bin_end)] = 0

                bins[(contig, bin_start, bin_end)] += abs(end - start)

    with open(output_file, 'w') as f:
        for (contig, bin_start, bin_end), segment_sum in bins.items():
            if remove_feat:
                f.write(f"{contig}\t{bin_start}\t{bin_end}\t{segment_sum}\n")
            else:
                f.write(f"{contig}\t{feature_type}\t{bin_start}\t{bin_end}\t{segment_sum}\n")

def main():
    parser = argparse.ArgumentParser(description='Generate bins from GFF file')
    parser.add_argument('-f', '--feature', required=True, help='Feature type to analyze')
    parser.add_argument('-b', '--bin_size', type=int, required=True, help='Bin size')
    parser.add_argument('-o', '--output_file', required=True, help='Output file name')
    parser.add_argument('-i', '--input_file', required=True, help='Input GFF file')
    parser.add_argument('--remove_feat', action='store_true', help='Remove feature column from output')

    args = parser.parse_args()
    process_gff_file(args.input_file, args.feature, args.bin_size, args.output_file, args.remove_feat)

if __name__ == "__main__":
    main()


# python Gen-Bin.py -f gene -b 50000 -o 50k_genes.txt -i rnd2_genes.gff #--remove_feat

#chr1    .       contig  1       69837        .       .       .       ID=xyz
#chr1    maker   gene    18497   19129   .       +       .       ID=xyz
#chr1    maker   mRNA    18497   19129   .       +       .       ID=xyz
#chr1    maker   exon    18497   19129   .       +       .       ID=xyz
#chr1    maker   CDS     18497   19129   .       +       0       ID=xyz
#chr1    maker   gene    35216   35488   .       +       .       ID=xyz
#chr1    maker   mRNA    35216   35488   .       +       .       ID=xyz
#chr1    maker   exon    35216   35488   .       +       .       ID=xyz
#chr1    maker   CDS     35216   35488   .       +       0       ID=xyz
#chr1    maker   gene    41499   42206   .       +       .       ID=xyz
#chr1    maker   mRNA    41499   42206   .       +       .       ID=xyz
#chr1    maker   exon    41499   41938   .       +       .       ID=xyz
#chr1    maker   exon    42008   42206   .       +       .       ID=xyz

#An example of what the result of this program will be when run with "Gen-Bin.py -f gene -b 20000 -o output_test.txt -i input.gff":
#chr1	gene	0	19999	632
#chr1	gene	20000	39999	272
#chr1	gene	40000	60000	707
#Where the first column is the specific contig for which bins are made (there will be more than one per input file), column 1 in the input.
#The second column of the output is the feature type selected from column 3 of the input.  The third and fourth column of the output is the interval of the contig
#in which the selected feature type is analyzed; it corresponds to the intervals of start and end coordinates in column 4 and 5 of the
#input.  Finally, the selected feature type will have its corresponding segments summed for each interval of bin size; 
#the absolute value of the difference between columns 4 and 5 of the input. in this example that is what is in column 5 of the output.

#--remove_feat = will delete column 2 and only leave the intervals for each contig and sum of nt of each feature