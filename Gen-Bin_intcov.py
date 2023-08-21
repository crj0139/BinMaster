#!/usr/bin/env python3

import argparse
import subprocess
import os

def calculate_average_coverage(coverage_data):
    total_coverage = sum(cov for _, cov in coverage_data)
    average_coverage = total_coverage / len(coverage_data)
    return average_coverage

def main():
    parser = argparse.ArgumentParser(description="Calculate average coverage over intervals.")
    parser.add_argument("-i", "--input", required=True, help="Input BAM file")
    parser.add_argument("-intv", "--bin_size", type=int, required=True, help="Bin size for intervals")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads for samtools index")
    parser.add_argument("-o", "--output_prefix", required=True, help="Output prefix for files")

    args = parser.parse_args()

    bam_file = args.input
    index_file = f"{bam_file}.bai"

    if not os.path.exists(bam_file):
        print(f"{bam_file} does not exist")
        return

    print(f"{bam_file} found and formatted correctly")

    if not os.path.exists(index_file):
        samtools_index_command = [
            "samtools",
            "index",
            "-b",
            "-@",
            str(args.threads),
            bam_file
        ]
        try:
            subprocess.run(samtools_index_command, check=True)
        except subprocess.CalledProcessError as e:
            print("Error running samtools index:", e)
            return

    samtools_idxstats_command = [
        "samtools",
        "idxstats",
        bam_file
    ]

    try:
        samtools_idxstats_output = subprocess.check_output(samtools_idxstats_command, text=True)
        contig_lengths = {}
        with open("contig_lengths.txt", "w") as contig_length_file:
            for line in samtools_idxstats_output.strip().split("\n"):
                fields = line.split("\t")
                # Skip lines starting with '*'
                if not fields[0].startswith('*'):
                    contig_lengths[fields[0]] = int(fields[1])
                    contig_length_file.write(f"{fields[0]}\t{fields[1]}\n")

        print("contig_lengths calculated, starting binning procedure")

        for chrom, contig_length in contig_lengths.items():
            print(f"Binning procedure for contig {chrom}")

            averaged_coverage = []

            for interval_start in range(1, contig_length + 1, args.bin_size):
                interval_end = min(interval_start + args.bin_size - 1, contig_length)

                print(f"Calculating interval {interval_start}-{interval_end} for contig {chrom}")

                samtools_command = [
                    "samtools",
                    "depth",
                    "-a",
                    "-r",
                    f"{chrom}:{interval_start}-{interval_end}",
                    bam_file
                ]
                
                try:
                    samtools_output = subprocess.check_output(samtools_command, text=True)
                    coverage_data = [line.split("\t") for line in samtools_output.strip().split("\n")]
                    coverage_data = [(int(pos), int(cov)) for _, pos, cov in coverage_data]

                    if coverage_data:
                        average_cov = calculate_average_coverage(coverage_data)
                        averaged_coverage.append((chrom, interval_start, interval_end, average_cov))
                        output_filename = f"{args.output_prefix}_{chrom}_averaged.txt"
                        with open(output_filename, "a") as output_file:
                            output_file.write(f"{chrom}\t{interval_start}\t{interval_end}\t{average_cov:.2f}\n")

                except subprocess.CalledProcessError as e:
                    print("Error running samtools:", e)

    except Exception as e:
        print("An error occurred:", e)

# Template shell command
# Gen-Bin_intcov.py -i <input_bam_file> -intv <bin_size> -t <threads> -o <output_prefix>

if __name__ == "__main__":
    main()




#./Gen-Bin_intcov.py -i test.s.bam -intv 50000 -o test.txt -t 2

