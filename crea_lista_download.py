import json

CS_CLASSES = [
    'cat:cs.' + cat for cat in [
        'AI', 'AR', 'CC', 'CE', 'CL', 'CR', 'CV',
        'DB', 'DC', 'DS', 'FL', 'GR', 'HC', 'IR',
        'IT', 'LG', 'LO', 'MA', 'MM', 'MS', 'NE',
        'NI', 'OS', 'PF', 'PL', 'SC', 'SD', 'SE', 'SI',
    ]
]

# Genera un dizionario con le categorie e un numero massimo di risultati predefinito
max_results_default = 5
download_config = {category: max_results_default for category in CS_CLASSES}

# Salva il dizionario in un file JSON
with open('Download.json', 'w', encoding='utf-8') as f:
    json.dump(download_config, f, indent=4)

print("Download.json generato con successo!")