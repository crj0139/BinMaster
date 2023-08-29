import argparse

def merge_intervals(intervals, max_gap):
    merged_intervals = []
    current_interval = intervals[0]
    
    for interval in intervals[1:]:
        if interval[1] - current_interval[2] <= max_gap and interval[0] == current_interval[0] and interval[3] == current_interval[3]:
            current_interval = (current_interval[0], current_interval[1], interval[2], current_interval[3], current_interval[4], interval[5])
        else:
            merged_intervals.append(current_interval)
            current_interval = interval
    
    merged_intervals.append(current_interval)
    return merged_intervals

def main():
    parser = argparse.ArgumentParser(description="Merge coordinate intervals between two chromosomes based on the distance between them.")
    parser.add_argument("-i", "--input", required=True, help="Input links file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("-c", "--max_gap", type=int, required=True, help="Maximum gap size allowed between merged blocks")
    args = parser.parse_args()
    
    with open(args.input, "r") as input_file:
        lines = input_file.readlines()
    
    intervals = []
    for line in lines:
        fields = line.strip().split("\t")
        intervals.append((fields[0], int(fields[1]), int(fields[2]), fields[3], int(fields[4]), int(fields[5])))
    
    merged_intervals = merge_intervals(intervals, args.max_gap)
    
    with open(args.output, "w") as output_file:
        for interval in merged_intervals:
            output_file.write("\t".join(map(str, interval)) + "\n")

if __name__ == "__main__":
    main()

#python Gen-Bin_syntenicblocker.py -i interspp.links.all.txt -o /mnt/c/Users/crj0139/Documents/Ubuntu/Software/circos-0.69-9/phyfe/interspp/interspp.links1663.txt -c 1663
