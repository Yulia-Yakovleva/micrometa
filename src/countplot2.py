import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='darkgrid')
width=10
height=6
plt.figure(figsize=(width,height))

df = pd.read_csv('/home/yulia/micrometa/results/full_metadata.tsv', sep=',')

sns.countplot(x='habitat', data=df, palette="Set3")
plt.title('Founded sequences in different habitats')
plt.xlabel('Habitats')
plt.xticks(rotation=70)
plt.ylabel('Counts')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('/home/yulia/micrometa/figures/habitats_ssu_countplot.pdf', format='pdf')
plt.savefig('/home/yulia/micrometa/figures/habitats_ssu_countplot.png', format='png', dpi=600)
plt.show() 
