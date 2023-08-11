# BinMaster Toolset

## BinMaster

Finds cumulative bases of any feature in a given bin size of a chromosome/contig.


#### Usage

```
python BinMaster.py -f <feature_type> -b 50000 -o <output_file> -i <input_gff> [--remove_feat]
    -f, --feature = Feature type to bin
    -b, --bin_size = Bin size desired along chromosome/contig
    -o, --output_file = output file, .txt works
    -i, --input_file = input .gff file
    --remove_feat - Remove feature column from output [optional, useful for Circos]
```
Where <feature_type> is the feature generally in column 3 of a .gff file.

For example, running BinMaster on this .gff file:
```
chr1    .       contig  1       69837        .       .       .       ID=xyz
chr1    maker   gene    18497   19129   .       +       .       ID=xyz
chr1    maker   mRNA    18497   19129   .       +       .       ID=xyz
chr1    maker   exon    18497   19129   .       +       .       ID=xyz
chr1    maker   CDS     18497   19129   .       +       0       ID=xyz
chr1    maker   gene    35216   35488   .       +       .       ID=xyz
chr1    maker   mRNA    35216   35488   .       +       .       ID=xyz
chr1    maker   exon    35216   35488   .       +       .       ID=xyz
chr1    maker   CDS     35216   35488   .       +       0       ID=xyz
chr1    maker   gene    41499   42206   .       +       .       ID=xyz
chr1    maker   mRNA    41499   42206   .       +       .       ID=xyz
chr1    maker   exon    41499   41938   .       +       .       ID=xyz
chr1    maker   exon    42008   42206   .       +       .       ID=xyz
```
using:
```
BinMaster.py -f gene -b 20000 -o output_test.txt -i input.gff
```
will give the output:
```
chr1	gene	0	19999	632
chr1	gene	20000	39999	272
chr1	gene	40000	60000	707
```

```--remove_feat``` = will delete column 2 and only leave the intervals for each contig and sum of nt of each feature, resulting in:
```
chr1	0	19999	632
chr1	20000	39999	272
chr1	40000	60000	707
```

## BinMaster_intcov

Calculates average read coverage over all intervals of user-specified length.


#### Usage
```
BinMaster_intcov.py -i <input_bam_file> -intv <bin_size> -t <threads> -o <output_prefix>
	-i = input bam file (if not indexed as .bam.bai first, BinMaster_intcov will do it for you)
	-intv = interval size over which to calculate average coverages
	-t = threads, used for samtools
	-o = output prefix
```

The output filename will be in format <output_prefix>_<contig_name>_averaged.txt, and a separate output will be 
made for all contigs.

The output file is formatted as so:
```
chr1	1	50000	90.01
chr1	50001	100000	34.58
chr1	100001	150000	30.00
chr1	150001	200000	90.62...
```
Where for this example, -intv of 50000 was used.  The fourth column contains the average read depth over that
entire interval, based on depth per individual nucleotide averaged over that interval.