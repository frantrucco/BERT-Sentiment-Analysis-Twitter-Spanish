from cleaner import clean
import sys
import mmap
from tqdm import tqdm


def get_num_lines(infile_path):
    with open(infile_path) as infile:
        num_lines = sum(1 for line in infile)
    return num_lines

if __name__ == '__main__':
    infile_path = sys.argv[1]
    outfile_path = sys.argv[2]

    total = get_num_lines(infile_path)

    with open(infile_path) as infile:
        with open(outfile_path, 'w') as outfile:
            for line in tqdm(infile, total=total):
                outfile.write(clean(line))
