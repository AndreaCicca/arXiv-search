import json
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

# Percorsi dei file
input_file = 'dataset/arxiv-metadata-oai-snapshot.json'
output_file = 'dataset/arxiv-computer-science.json'
chunk_size = 500  # Numero di righe per blocco

def filter_chunk(chunk):
    cs_papers = []
    for line in chunk:
        paper = json.loads(line)
        if any(category.startswith('cs') for category in paper['categories'].split()):
            cs_papers.append(paper)
    return cs_papers

def filter_computer_science_papers(input_file, output_file, chunk_size):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(filter_chunk, chunks), total=len(chunks)))
    
    cs_papers = [paper for result in results for paper in result]
    
    with open(output_file, 'w') as outfile:
        for paper in cs_papers:
            json.dump(paper, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    filter_computer_science_papers(input_file, output_file, chunk_size)
    
