# gene-to-protein-domains

## Overview

This tool retrieves protein domain positions and transcript information for a given human gene and outputs the results as TSV tables. It uses the UniProt, InterPro, and Ensembl APIs to fetch reviewed protein entries, their domain annotations, and transcript details.

**Note:** This script only works for human genes (Homo sapiens, taxonomy_id:9606, reviewed entries only).

## Setup

**Clone the repository:**

```bash
git clone https://github.com/maurya-anand/gene-to-protein-domains.git
cd gene-to-protein-domains
```

## Requirements

- Python 3
- Internet connection (to access UniProt, InterPro, and Ensembl APIs)
- All required Python modules (`sys`, `os`, `json`, `urllib.request`, `argparse`, `logging`, `time`) are part of the Python standard library.

## Usage

Run the script from the command line:

```sh
python gene-to-protein-domains.py --gene GENE_NAME [--hide TYPE1,TYPE2,...] [--fetch domain|transcript|both] [--retries N]
```

### Arguments

- `--gene` (required): Gene name to search (e.g. NOTCH1, BRCA1).
- `--hide` (optional): Comma-separated values to hide by 'Type' column in the domain table (e.g. family,repeat,domain).  
  **Note:** Only valid when `--fetch` is `domain` or `both`.
- `--fetch` (optional): Which information to fetch: `domain`, `transcript`, or `both` (default: `both`).
- `--retries` (optional): Number of times to retry API requests on failure (default: 3).

### Examples

```sh
# Retrieve all domains and transcript info for NOTCH1
python gene-to-protein-domains.py --gene NOTCH1

# Hide 'family' and 'repeat' types in domain output
python gene-to-protein-domains.py --gene NOTCH1 --hide family,repeat

# Only fetch transcript info for BRCA1
python gene-to-protein-domains.py --gene BRCA1 --fetch transcript

# Only fetch domain info for BRCA1, retrying up to 5 times on API failure
python gene-to-protein-domains.py --gene BRCA1 --fetch domain --retries 5
```

## Output

The outputs are TSV tables:

- `<gene_name>_domain.tsv` — Protein domain annotation table (if `--fetch domain` or `both`)
- `<gene_name>_transcript.tsv` — Transcript annotation table (if `--fetch transcript` or `both`)

### `<gene_name>_domain.tsv`

| query_gene | uniprot_id | pfam_accession | name | source_database | type | integrated_id | go_terms | protein_accession | protein_length | entry_protein_locations_count | start | end |
| :--------- | :--------- | :------------- | :--- | :-------------- | :--- | :------------ | :------- | :---------------- | :------------- | :---------------------------- | :---- | :-- |
| --         | --         | --             | --   | --              | --   | --            | --       | --                | --             | --                            | --    | --  |

Rows are sorted by the fragment start position.

### `<gene_name>_transcript.tsv`

A simple key-value TSV table with transcript and gene information from Ensembl.  
**Note:** The transcript TSV does not include a header row.

```tsv
assembly_name -
biotype -
canonical_transcript -
db_type -
description -
display_name -
end -
id -
logic_name -
object_type -
seq_region_name -
source -
species -
start -
strand -
version -
```

## API Sources

- [UniProt REST API](https://rest.uniprot.org/)
- [InterPro API](https://www.ebi.ac.uk/interpro/api/)
- [Ensembl REST API](https://rest.ensembl.org/)

## Troubleshooting

- If you receive "No UniProt ID found for gene" or "No Ensembl gene ID found for gene", check the gene name and ensure it is a reviewed human gene in UniProt/Ensembl.
- If you experience network issues, increase the `--retries` value.
