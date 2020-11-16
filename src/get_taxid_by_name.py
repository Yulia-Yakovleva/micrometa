import pandas as pd

prefs = ['ssu', 'lsu']

dump = {}

print('Create taxonomy dictionary...')
with open('/home/yulia/micrometa/names.dmp') as in_f:
    for line in in_f:
        line = line.strip()
        words = line.split('\t')
        dump[words[2]] = words[0]
print('Create taxonomy dictionary... Done')


def check_tax(tax):
    for el in reversed(tax):
        if el == 'Unclassified':
            return 'Unclassified'
        elif el in set(dump.keys()):
            return(dump[el])
        else:
            pass
            
def create_set_dict(custom_set):
    print("Creating set_dict...")
    set_dict = {}
    for count, el in enumerate(custom_set):
        print(f'Working with element...\t{count} / {len(custom_set)}', end='\r')
        tax = el.split(';')
        val = check_tax(tax)
        set_dict[el] = val
    print("Creating set_dict...\tDone")
    return set_dict


for pref in prefs:
    print(f'Working with {pref} file...')
    tax_set = set()
    with open(f'{pref}_sina_for_krona.out', 'w') as out_f:
        df = pd.read_csv(f'/home/yulia/micrometa/sina/aligned_{pref}.csv')
        print("Creating tax_set...")
        for taxonomy in df.lca_tax_slv:
            if taxonomy not in tax_set:
                tax_set.add(taxonomy)
        print(f"Creating tax_set...\tThe length of tax_set is {len(tax_set)}")
        set_dict = create_set_dict(tax_set)
        for count, (read, taxonomy) in enumerate(zip(df.name, df.lca_tax_slv)):
            taxid = set_dict[taxonomy]   
            #print(taxid)
            out_f.write(f"{read}\t{taxid}\n")
            print(f'Working with {pref} file...\t{count} / {len(df.name)}', end='\r')
    print('Deal with it!')

print('Done.')
