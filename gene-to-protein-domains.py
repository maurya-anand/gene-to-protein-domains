
#!/usr/bin/env python3

"""
Retrieve protein domain positions for a gene and output as TSV.

NOTE: This script only works for human genes (Homo sapiens, taxonomy_id:9606, reviewed entries only).
"""
import sys
import os
import json
import urllib.request
import argparse

class ProteinDomainFetcher:
    """
    Fetch and display protein domain information for a given human gene using UniProt and InterPro APIs.

    NOTE:
        This script only works for human genes (Homo sapiens, taxonomy_id:9606, reviewed entries only).

    Args:
        gene_name (str): The gene name to search for (e.g., 'NOTCH1').
        hide_types (str, optional): Comma-separated string of domain types to hide (e.g., 'family,repeat').

    Example:
        fetcher = ProteinDomainFetcher('NOTCH1', 'family,repeat')
        fetcher.run()
    """
    def __init__(self, gene_name, hide_types=None):
        """
        Initialize the fetcher with a gene name and optional types to hide.

        Args:
            gene_name (str): The gene name to search for (e.g., 'NOTCH1').
            hide_types (str, optional): Comma-separated string of domain types to hide (e.g., 'family,repeat').
        """
        self.gene_name = gene_name
        self.hide_types = hide_types
        self.uniprot_id = None
        self.results = None

    def get_uniprot_id(self):
        """
        Retrieve the UniProt ID for the gene name (human, reviewed entries only).

        Returns:
            str or None: UniProt accession string if found, else None.

        Note:
            Only reviewed human entries are considered.

        Example:
            uniprot_id = self.get_uniprot_id()
        """
        url = (
            f"https://rest.uniprot.org/uniprotkb/stream?fields=accession&format=tsv"
            f"&query=((gene:{self.gene_name})+AND+(taxonomy_id:9606)+AND+(reviewed:true))"
        )
        with urllib.request.urlopen(url) as response:
            lines = response.read().decode().strip().split("\n")
        if len(lines) < 2:
            return None
        return lines[1].strip()

    def get_domains(self):
        """
        Retrieve domain information from InterPro for the UniProt ID.

        Returns:
            dict: Parsed JSON response from InterPro API.

        Note:
            Requires self.uniprot_id to be set.

        Example:
            domains = self.get_domains()
        """
        url = f"https://www.ebi.ac.uk/interpro/api/entry/pfam/protein/UniProt/{self.uniprot_id}/?page_size=200"
        with urllib.request.urlopen(url) as response:
            return json.load(response)

    def print_table(self):
        """
        Print the domain information as a TSV table, optionally hiding specified types. Output is sorted by fragment start position.

        Args:
            None (uses self.results and self.hide_types)

        Note:
            Prints to standard output. Output is sorted by fragment start.

        Example:
            self.print_table()
        """
        header = [
            "query_gene", "uniprot_id", "pfam_accession", "name", "source_database", "type", "integrated_id", "go_terms",
            "protein_accession", "protein_length", "entry_protein_locations_count",
            "start", "end"
        ]
        print("\t".join(header))
        hide_types_set = set()
        if self.hide_types:
            hide_types_set = set(t.strip().lower() for t in self.hide_types.split(",") if t.strip())
        rows = set()
        for entry in self.results.get('results', []):
            meta = entry["metadata"]
            typ = meta.get("type", "").lower()
            if typ in hide_types_set:
                continue
            for prot in entry["proteins"]:
                locations = prot.get("entry_protein_locations", [])
                loc_count = len(locations)
                for loc in locations:
                    for frag in loc.get("fragments", []):
                        row = (
                            self.gene_name,
                            self.uniprot_id,
                            meta.get("accession", ""),
                            meta.get("name", ""),
                            meta.get("source_database", ""),
                            meta.get("type", ""),
                            str(meta.get("integrated", "")),
                            str(meta.get("go_terms", "")),
                            prot.get("accession", ""),
                            str(prot.get("protein_length", "")),
                            str(loc_count),
                            str(frag.get("start", "")),
                            str(frag.get("end", ""))
                        )
                        rows.add(row)
        # Sort rows by fragment start (column 11, as int)
        sorted_rows = sorted(rows, key=lambda r: int(r[11]) if r[11].isdigit() else float('inf'))
        for row in sorted_rows:
            print("\t".join(row))

    def run(self):
        """
        Run the full workflow: fetch UniProt ID, fetch domains, and print the table.

        Args:
            None

        Note:
            Exits the program if the gene is not found.

        Example:
            fetcher = ProteinDomainFetcher('NOTCH1')
            fetcher.run()
        """
        self.uniprot_id = self.get_uniprot_id()
        if not self.uniprot_id:
            print(f"No UniProt ID found for gene: {self.gene_name}", file=sys.stderr)
            sys.exit(1)
        self.results = self.get_domains()
        self.print_table()



def main():
    """
    Parse command-line arguments and run the ProteinDomainFetcher.

    Args:
        None (uses sys.argv)

    Example:
        python {script_name} --gene NOTCH1 --hide family,repeat
    """
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description=(
            f"Retrieve protein domain positions for a gene and output as TSV.\n"
            f"\n"
            f"NOTE: This script works with human genes (Homo sapiens, taxonomy_id:9606, reviewed entries only) from UniProt.\n"
            f"\n"
            f"Examples:\n"
            f"  python {script_name} --gene NOTCH1\n"
            f"  python {script_name} --gene NOTCH1 --hide family,repeat\n"
            f"  python {script_name} --gene BRCA1 --hide domain\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--gene', required=True,
        help="Gene name to search (e.g. NOTCH1, BRCA1). Example: --gene NOTCH1"
    )
    parser.add_argument(
        '--hide', default=None,
        help="Comma-separated values to hide by 'Type' column (e.g. family,repeat). Example: --hide family,repeat"
    )
    args = parser.parse_args()

    fetcher = ProteinDomainFetcher(args.gene.upper(), args.hide)
    fetcher.run()

if __name__ == "__main__":
    main()
