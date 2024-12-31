import pandas as pd
from datetime import datetime

CS_CLASSES = [
    'cs\\.' + cat for cat in [
        'AI', 'AR', 'CC', 'CE', 'CL', 'CR', 'CV',
        'DB', 'DC', 'DS', 'FL', 'GR', 'HC', 'IR',
        'IT', 'LG', 'LO', 'MA', 'MM', 'MS', 'NE',
        'NI', 'OS', 'PF', 'PL', 'SC', 'SD', 'SE', 'SI',
        # 'CV', 'LG', 'CL', 'AI', 'NE', 'RO' # shorter ai list
    ]
]
pattern = '|'.join(CS_CLASSES)

print('Loading dataset....')
df = pd.read_json('arxiv-metadata-oai-snapshot.json',lines=True)
print('Dataset loaded!')

df['created'] = df['versions'].apply(lambda x: (x[0]['created']))
df['created'] = pd.to_datetime(df['created'], format="%a, %d %b %Y %H:%M:%S GMT")
df['created'] = df['created'].dt.strftime('%Y-%m-%d')


start_date = '2023-01-01'

#df = df[df['update_date'] >= start_date] 
df = df[df['created'] >= start_date] 
print(df.shape)

df = df[df['categories'].str.contains(pattern)]

print(df.shape)

df.to_json('cs-23-24.json')