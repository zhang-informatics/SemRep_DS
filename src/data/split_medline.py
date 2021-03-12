import os
import argparse


"""
Splits a single file of MEDLINE formatted abstracts
into M files of N abstracts.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="MEDLINE file to split")
    parser.add_argument("outdir", type=str,
                        help="Where to save the file splits.")
    parser.add_argument("-N", type=int, default=100,
                        help="Number of abstracts per file.")
    parser.add_argument("-M", type=int, default=None,
                        help="Maximum number of files.")
    return parser.parse_args()


def main(args):
    with open(args.infile, 'r') as inF:
        file_counter = 0
        buf = []
        nread = 0
        for (i, line) in enumerate(inF):
            if args.M is not None and file_counter >= args.M:
                break
            print(f"{file_counter}\r", end='', flush=True)
            line = line.strip()
            if line == '':
                if i == 0:  # Skip initial blank lines.
                    continue
                nread += 1
            buf.append(line)
            if nread >= args.N and line == '':
                outfile = f"out{file_counter:>04d}.txt"
                outpath = os.path.join(args.outdir, outfile)
                with open(outpath, 'w') as outF:
                    outF.write('\n'.join(buf))
                buf = []
                nread = 0
                file_counter += 1

        if len(buf) > 0:
            outfile = f"out{file_counter:>04d}.txt"
            outpath = os.path.join(args.outdir, outfile)
            with open(outpath, 'w') as outF:
                outF.write('\n'.join(buf))


if __name__ == "__main__":
    args = parse_args()
    main(args)
