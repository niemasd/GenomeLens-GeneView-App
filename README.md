# GeneView #

### Description
---
GeneView is an app for the upcoming "GenomeLens" project (Linux x64). Given the variant information imported into GenomeLens, GeneView will display gene-by-gene visualizations (generated using [lollipops](https://github.com/pbnjay/lollipops)) for every gene provided.

### Usage
---
0) Download package and extract into a folder

1) Mark "lollipops" as executable: chmod +x lollipops

2) Run GeneView: GeneView.py <input_file>

Currently, GeneView requires an input file where each row corresponds to a specific mutation. The left column is the gene name, and the right column is the protein-level annotation of the mutation. When GenomeLens is completed, the script will be modified to access the GenomeLens database directly.