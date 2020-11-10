from Bio import SeqIO
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='whitegrid')

pth = '/home/yulia/micrometa/sina/'
out = '/home/yulia/micrometa/figures/'

files = ['ssu_interesting.fasta', 'lsu_interesting.fasta', 'euk_interesting.fasta']

for f in files:
    lens = tuple(len(rec) for rec in SeqIO.parse(pth+f, 'fasta'))
    sns.distplot(lens, kde=False)
    # plt.hist(lens, bins=np.logspace(np.log10(min(lens)), np.log10(max(lens)), 52), alpha=0.5)
    # plt.gca().set_xscale("log")
    # plt.subplots_adjust(bottom=0.14, top=0.98, right=0.99, left=0.17)

    plt.ylabel('Number of sequences')
    plt.xlabel('Length')
    plt.title(f"Length distribution of founded {f[:3]} sequences")
    plt.savefig(f"{out}{f[:3]}_len_dist.pdf", format='pdf')
    plt.savefig(f"{out}{f[:3]}_len_dist.png", format='png', dpi=600)
    plt.show()
