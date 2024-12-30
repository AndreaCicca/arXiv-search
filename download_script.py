import os
import time
import json
import requests
import feedparser
from markitdown import MarkItDown
from datetime import datetime
from dateutil.relativedelta import relativedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, Back, init

# Inizializza colorama
init(autoreset=True)

CS_CLASSES = [
    'cs.' + cat for cat in [
        'AI', 'AR', 'CC', 'CE', 'CG', 'CL', 'CR', 'CV', 'CY', 'DB',
        'DC', 'DL', 'DM', 'DS', 'ET', 'FL', 'GL', 'GR', 'GT', 'HC',
        'IR', 'IT', 'LG', 'LO', 'MA', 'MM', 'MS', 'NA', 'NE', 'NI',
        'OH', 'OS', 'PF', 'PL', 'RO', 'SC', 'SD', 'SE', 'SI', 'SY',
    ]
]

end_date = datetime.now()
start_date = end_date - relativedelta(years=2)

end_str = end_date.strftime('%Y-%m-%d')
start_str = start_date.strftime('%Y-%m-%d')


def safe_request(url, max_retries=3, backoff_factor=2):
    """Esegue una richiesta HTTP in modo sicuro, ritentando in caso di errori."""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code and 500 <= status_code < 600 and attempt < max_retries:
                wait_time = backoff_factor * attempt
                print(f"{Fore.YELLOW}Errore server {status_code}, tentativo {attempt}/{max_retries}. Attendo {wait_time} secondi...")
                time.sleep(wait_time)
            else:
                print(f"{Fore.RED}Errore HTTP irreversibile su {url}: {e}")
                return None
        except requests.ConnectionError as e:
            if attempt < max_retries:
                wait_time = backoff_factor * attempt
                print(f"{Fore.YELLOW}Errore di connessione, tentativo {attempt}/{max_retries}. Attendo {wait_time} secondi...")
                time.sleep(wait_time)
            else:
                print(f"{Fore.RED}Connessione fallita su {url} dopo {max_retries} tentativi: {e}")
                return None
    return None

def download_arxiv_data(query, start=0, max_results=5,
                        pdf_output_dir="arxiv_pdfs", md_output_dir="arxiv_markdowns", json_output_dir="arxiv_metadata"):
    # Costruisci l'URL per la query di arXiv
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{query} AND lastUpdatedDate:[{start_str} TO {end_str}]&"
        f"start={start}&"
        f"max_results={max_results}&"
        f"sortOrder=descending"
    )
    
    print(f"{Fore.CYAN}Scarico i risultati da: {url}")
    
    response = safe_request(url)
    if not response:
        print(f"{Fore.RED}Impossibile ottenere i risultati da arXiv. Interrompo.")
        return
    
    data = response.text
    
    # Parsing del feed atom tramite feedparser
    feed = feedparser.parse(data)
    
    # Creazione delle cartelle di destinazione se non esistono
    for output_dir in [pdf_output_dir, md_output_dir, json_output_dir]:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    md = MarkItDown()  # Inizializza il convertitore Markdown
    
    for entry in feed.entries:
        pdf_link = None
        for link in entry.links:
            if link.type == "application/pdf":
                pdf_link = link.href
                break
        
        article_id = entry.id.split('/')[-1]
        
        # Salva i metadati in JSON
        metadata = {
            "id": entry.id,
            "updated": entry.updated,
            "published": entry.published,
            "title": entry.title,
            "summary": entry.summary,
            "authors": [{"name": author.name, "affiliation": getattr(author, "arxiv_affiliation", None)} for author in entry.authors],
            "doi": getattr(entry, "arxiv_doi", None),
            "comment": getattr(entry, "arxiv_comment", None),
            "journal_ref": getattr(entry, "arxiv_journal_ref", None),
            "primary_category": getattr(entry, "arxiv_primary_category", {}).get("term", None),
            "categories": [cat["term"] for cat in getattr(entry, "tags", [])],
            "pdf_link": pdf_link
        }
        
        json_path = os.path.join(json_output_dir, f"{article_id}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(metadata, json_file, indent=4)
        print(f"{Fore.GREEN}Salvati metadati: {json_path}")
        
        if pdf_link:
            pdf_path = os.path.join(pdf_output_dir, f"{article_id}.pdf")
            
            pdf_response = safe_request(pdf_link)
            if pdf_response:
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"{Fore.GREEN}Scaricato: {pdf_path}")
                
                # Tenta la conversione in markdown
                try:
                    result = md.convert(pdf_path)
                    md_content = result.text_content
                    
                    md_path = os.path.join(md_output_dir, f"{article_id}.md")
                    with open(md_path, 'w', encoding='utf-8') as f_md:
                        f_md.write(md_content)
                    
                    print(f"{Fore.GREEN}Convertito in Markdown: {md_path}")
                except Exception as e:
                    print(f"{Fore.RED}Impossibile convertire {pdf_path} in Markdown: {e}")
            else:
                print(f"{Fore.RED}Non è stato possibile scaricare il PDF per {entry.id}. Passo al prossimo.")
        else:
            print(f"{Fore.RED}Nessun PDF disponibile per: {entry.title}")


# Carica le categorie e i numeri massimi di risultati dal file JSON
with open('Download.json', 'r', encoding='utf-8') as f:
    download_config = json.load(f)

if __name__ == "__main__":
    num_threads = os.cpu_count() or 1
    
    print(f"{Fore.CYAN}Numero di Thread: {num_threads}")
    print(f"{Fore.GREEN}Scarico i risultati per le seguenti categorie di arXiv: {list(download_config.keys())}")
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(download_arxiv_data, query=query, max_results=max_results) for query, max_results in download_config.items()]
        for future in as_completed(futures):
            future.result()