import glob
import pandas as pd
from subprocess import Popen, PIPE

pth = '/home/yulia/micrometa/metadata/'

df = pd.DataFrame(columns=['seq_name', 'type', 'habitat'])

for filename in glob.glob(pth+'*.lst'):
    stdout, stderr = Popen(["wc", "-l", filename], stdout=PIPE).communicate()
    file_length = stdout.decode("utf-8").split(' ')[0]
    habitat = filename.split('/')[-1].replace('.lst', '')
    print(f'Working with habitat {habitat}...')
    with open(filename, 'r') as in_f:
        for count, line in enumerate(in_f):
            seq_name = line.strip().replace('>', '')
            gene = seq_name.split('_rRNA')[0]
            print(f'Working with habitat {habitat}...\t{count} / {file_length}', end='\r')
            #print(f"{seq_name}\t{gene}\t{habitat}")
            df = df.append({'seq_name': seq_name,
                            'type': gene,
                            'habitat': habitat},
            ignore_index=True)        

print(df)
df.to_csv(pth+'habitat_info.tsv', sep='\t')
