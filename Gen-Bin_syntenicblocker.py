import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate simplified linkage data.")
    parser.add_argument("-i", "--input", type=str, help="Input text file")
    parser.add_argument("-intv", "--int_size", type=int, help="Interval size")
    parser.add_argument("-o", "--output", type=str, help="Output text file")
    return parser.parse_args()

def process_data(input_file, int_size, output_file):
    interval_links = {}

    with open(input_file, "r") as f:
        for line in f:
            fields = line.strip().split()
            chr1, start1, end1, chr2, start2, end2 = fields
            start1 = int(start1)
            start2 = int(start2)
            interval1 = start1 // int_size
            interval2 = start2 // int_size

            interval_pair = (chr1, interval1, chr2, interval2)
            if interval_pair in interval_links:
                interval_links[interval_pair] += 1
            else:
                interval_links[interval_pair] = 1

    with open(output_file, "w") as f:
        for (chr1, interval1, chr2, interval2), count in interval_links.items():
            start1 = interval1 * int_size + 1
            end1 = start1 + int_size - 1
            start2 = interval2 * int_size + 1
            end2 = start2 + int_size - 1
            f.write(f"{chr1} {start1} {end1} {chr2} {start2} {end2} {count}\n")

if __name__ == "__main__":
    args = parse_args()
    process_data(args.input, args.int_size, args.output)

#python Gen-Bin_syntenicblocker.py -i pf.links.txt -intv 1000000 -o pf.links.blocked.txt
