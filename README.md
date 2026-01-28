# gene-to-protein-domains

## Overview

This tool retrieves protein domain positions for a given human gene and outputs the results as a TSV table. It uses the UniProt and InterPro APIs to fetch reviewed protein entries and their domain annotations.

**Note:** This script only works for human genes (Homo sapiens, taxonomy_id:9606, reviewed entries only).

## Setup

**Clone the repository:**

```bash
git clone https://github.com/your-username/gene-to-protein-domains.git
cd gene-to-protein-domains
```

## Requirements

- Python 3
- Internet connection (to access UniProt and InterPro APIs)
- All required Python modules (`sys`, `os`, `json`, `urllib.request`, `argparse`) are part of the Python standard library.

## Usage

Run the script from the command line:

```sh
python gene-to-protein-domains.py --gene GENE_NAME [--hide TYPE1,TYPE2,...]
```

### Arguments

- `--gene` (required): Gene name to search (e.g. NOTCH1, BRCA1).
- `--hide` (optional): Comma-separated values to hide by 'Type' column (e.g. family,repeat,domain).

### Examples

```sh
# Retrieve all domains for NOTCH1
python gene-to-protein-domains.py --gene NOTCH1

# Hide 'family' and 'repeat' types
python gene-to-protein-domains.py --gene NOTCH1 --hide family,repeat

# Hide 'domain' type for BRCA1
python gene-to-protein-domains.py --gene BRCA1 --hide domain
```

## Output

The output is a TSV table with the following columns:

| query_gene | uniprot_id | pfam_accession | name | source_database | type | integrated_id | go_terms | protein_accession | protein_length | entry_protein_locations_count | start | end |
| :--------- | :--------- | :------------- | :--- | :-------------- | :--- | :------------ | :------- | :---------------- | :------------- | :---------------------------- | :---- | :-- |
| --         | --         | --             | --   | --              | --   | --            | --       | --                | --             | --                            | --    | --  |

Rows are sorted by the fragment start position.

## Notes

- Only reviewed human entries are considered (taxonomy_id:9606, reviewed:true).
- The script will exit with an error if the gene is not found in UniProt.
- Data is fetched live from UniProt and InterPro APIs.

## API Sources

- [UniProt REST API](https://rest.uniprot.org/)
- [InterPro API](https://www.ebi.ac.uk/interpro/api/)

## Troubleshooting

- If you receive "No UniProt ID found for gene", check the gene name and ensure it is a reviewed human gene in UniProt.
