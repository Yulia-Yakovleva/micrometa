import argparse
from Bio import SeqIO


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check queries without blast hits')
    parser.add_argument('-infa', '--input_fasta', type=str, help='Input fasta file')
    parser.add_argument('-inlist', '--input_list', type=str, help='Input list of names file')
    args = parser.parse_args()

    names = []
    with open(args.input_list, 'r') as in_f:
        for line in in_f:
            name = line.strip()
            names.append(name)

    print(names)

    with open('interesting.fasta', 'w') as out_f:
        recs = SeqIO.parse(args.input_fasta, 'fasta')
        for rec in recs:
            if rec.name in names:
                rec.id = rec.name
                rec.name = ''
                rec.description = ''
                print(rec)
                SeqIO.write(rec, out_f, 'fasta')
