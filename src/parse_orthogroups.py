import pandas as pd
import numpy as np

from Bio import SeqIO
from glob import glob
from Bio.SeqRecord import SeqRecord
from collections import defaultdict
from os.path import basename, splitext

orthogroups = pd.read_csv('/Bmo/jyakovleva/bacillus/proteinortho_results_STRICT/myproject.proteinortho.tsv', sep='\t')
proteins_folder = '/Bmo/jyakovleva/bacillus/faa_data/'
used_columns = 3


def make_index(used_proteins):
    id_to_indexes = defaultdict(dict)
    for gbff_path in glob('/Bmo/jyakovleva/bacillus/gbff_data/' + '*.gbff'):
        gbff_name = basename(gbff_path)
        records = SeqIO.parse(gbff_path, 'genbank')

        for record in records:
            for feature in record.features:
                if feature.type == 'CDS' and 'protein_id' in feature.qualifiers and feature.qualifiers['protein_id'][0] in used_proteins:
                    q = feature.qualifiers
                    protein_id = q['protein_id'][0]
                    location = feature.location
                    species = splitext(gbff_name)[0]

                    seq = record.seq[location.start:location.end]
                    if location.strand == -1:
                        seq = seq.reverse_complement()
                    if not 'join' in str(location):
                        id_to_indexes[species][protein_id] = seq
    return id_to_indexes


# number of genomes (without basic column names)
true_columns = orthogroups.columns[used_columns:]
n = len(true_columns)

valid = 0

us = []
for i, row in orthogroups.iterrows():
    if not row['Genes'] == row['# Species'] == n: continue
    us.append(len(np.unique(row.values[used_columns:])))

threshold = np.percentile(us, 90)

used_proteins = set()
valid = 0
for i, row in orthogroups.iterrows():
    if not row['Genes'] == row['# Species'] == n: continue
    proteins = row.values[used_columns:]
    unique_proteins = np.unique(proteins)
    if len(unique_proteins) < threshold: continue

    [used_proteins.add(protein_id) for protein_id in proteins]
    valid += 1

print(valid)

id_to_indexes = make_index(used_proteins)
print('Index is done')

for i, row in orthogroups.iterrows():
    if not row['Genes'] == row['# Species'] == n: continue
    proteins = row.values[used_columns:]
    unique_proteins = np.unique(proteins)
    if len(unique_proteins) < threshold: continue

    if all(p_id in id_to_indexes[splitext(sp)[0]] for sp, p_id in zip(true_columns, proteins)):
        seqs = [SeqRecord(id_to_indexes[splitext(sp)[0]][p_id], splitext(sp)[0], '', '')
                                                for sp, p_id in zip(true_columns, proteins)]

        SeqIO.write(seqs, f'/Bmo/jyakovleva/bacillus/ortho_groups_STRICT/orthogroup_{i}.fasta', 'fasta')
