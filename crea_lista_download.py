import json

CS_CLASSES = [
    'cs.' + cat for cat in [
        'AI', 'AR', 'CC', 'CE', 'CG', 'CL', 'CR', 'CV', 'CY', 'DB',
        'DC', 'DL', 'DM', 'DS', 'ET', 'FL', 'GL', 'GR', 'GT', 'HC',
        'IR', 'IT', 'LG', 'LO', 'MA', 'MM', 'MS', 'NA', 'NE', 'NI',
        'OH', 'OS', 'PF', 'PL', 'RO', 'SC', 'SD', 'SE', 'SI', 'SY',
    ]
]

# Genera un dizionario con le categorie e un numero massimo di risultati predefinito
max_results_default = 5
download_config = {category: max_results_default for category in CS_CLASSES}

# Salva il dizionario in un file JSON
with open('Download.json', 'w', encoding='utf-8') as f:
    json.dump(download_config, f, indent=4)

print("Download.json generato con successo!")