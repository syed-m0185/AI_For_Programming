"""Print the GC content of each sequence in a FASTA file."""

import argparse
import warnings


def report_record(header, sequence, min_gc):
    """Print a record's GC percentage, or warn if its sequence is empty."""
    if not sequence:
        warnings.warn(f"Skipping empty sequence for {header}", stacklevel=2)
        return

    gc_count = sum(base in "GC" for base in sequence.upper())
    percentage = gc_count / len(sequence) * 100
    if min_gc is None or percentage > min_gc:
        print(f"{header}: {percentage:.2f}%")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta_file", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc", type=float, help="only print records above this GC percentage"
    )
    args = parser.parse_args()

    header = None
    sequence = []
    with open(args.fasta_file, encoding="utf-8") as fasta:
        for line in fasta:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    report_record(header, "".join(sequence), args.min_gc)
                header = line
                sequence = []
            elif header is not None:
                sequence.append(line)

    if header is not None:
        report_record(header, "".join(sequence), args.min_gc)


if __name__ == "__main__":
    main()
