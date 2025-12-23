**#1** transcriptome_pipeline.sh

_🧬 RNA-Seq Alignment and Quantification Pipeline:_

A lightweight and automated RNA-Seq data processing pipeline written in Bash, designed for reproducible transcriptome analysis.
It takes an SRA ID, performs QC, alignment, and gene quantification, and outputs ready-to-analyze count tables.

🚀 Features:
🔹 Automatic FASTQ extraction from SRA
🔹 Quality control & trimming using fastp
🔹 Genome indexing and alignment using Subread/Subjunc
🔹 Read quantification with featureCounts
🔹 Multi-threaded execution with auto CPU detection
🔹 Step-skipping for faster reruns (checks for existing outputs)

⚙️ Pipeline Workflow:
SRA_ID → fasterq-dump → fastp → subread-buildindex → subjunc → samtools sort → featureCounts

📦 Dependencies:

| Tool        | Purpose                                                                                         |
| ----------- | ----------------------------------------------------------------------------------------------- |
| `sra-tools` | Download and convert SRA to FASTQ                                                               |
| `fastp`     | Quality control and adapter trimming                                                            |
| `subread`   | Genome indexing (`subread-buildindex`), alignment (`subjunc`), quantification (`featureCounts`) |
| `samtools`  | BAM conversion and sorting                                                                      |

🧰 Input Requirements:                                                            
| File       | Description               | Example           |                        
| ---------- | ------------------------- | ----------------- |
| **FASTA**  | Reference genome sequence | `sequences.fasta` |
| **GTF**    | Genome annotation file    | `genome.gtf`      |
| **SRA ID** | Accession from NCBI SRA   | `SRR********`     |


📁 Output Files:
| Output File                              | Description              |
| ---------------------------------------- | ------------------------ |
| `*_1.trimmed.fastq`, `*_2.trimmed.fastq` | Trimmed paired-end reads |
| `*_fastp.html`, `*_fastp.json`           | Quality reports          |
| `*_index.*`                              | Genome index files       |
| `*_aln_sorted.bam`                       | Sorted BAM alignment     |
| `*_featureCounts_output.txt`             | Gene-level read counts   |


**#2** heatmap_GOI –-> for selected genes.

Features:
  Directly written in R.
  Converts .ods input files to .csv using LibreOffice (headless mode).
  Generates a heatmap for a user-defined list of genes.
  Simple clustering: rows and columns are not clustered.
  Easy for small, targeted gene sets.

Usage:
  genes_of_interest <- c("WASH9P", "MIR12136", "OR4F16")


**#3** heatmaps_n-genes.py --> automatically selects the most variable genes.

A lightweight, cross-language tool that generates publication-ready heatmaps of the top variable genes from an expression matrix.
Built with Python + R, this script automates preprocessing, normalization, and visualization of gene expression data.

📖 Overview:
This script reads a gene expression matrix (.csv, .txt, or .ods), filters and normalizes it, selects the most variable genes, and produces a clustered heatmap using R’s pheatmap.
The resulting heatmap highlights expression trends and sample clustering, aiding quick interpretation of transcriptomic data.

⚙️ How It Works:
File Detection – The script automatically detects the file format (.csv, .txt, .ods).
Data Cleaning – Removes empty columns, non-numeric data, and missing-value rows.
Transformation – Applies log₂(x + 1) normalization to stabilize variance.
Gene Selection – Computes variance for each gene and selects the top N most variable genes (default = 50).
Heatmap Generation – Uses pheatmap() with Euclidean distance and complete linkage clustering.
Output – Saves a ready-to-use PDF named heatmap_output.pdf.

🧩 Requirements:
System
  Python 3
  R (must be available in your system PATH)
R Packages(Installed automatically if missing):
  pheatmap
  readODS (required only for .ods files)

🚀 Usage:
./heatmaps.py <expression_matrix.(txt|csv|ods)> [top_n]
eg:
./heatmaps.py expression_data.txt 100

Format of featurecounts file:
| Gene   | Sample1 | Sample2 | Sample3 | ... |
|---------|----------|----------|----------|-----|
| GENE1  | 4.5      | 5.2      | 6.1      |     |
| GENE2  | 2.1      | 3.8      | 1.5      |     |
| ...    |          |          |          |     |
   


🖼️ Output:
File: heatmap_output.pdf
Content: Hierarchically clustered heatmap of top variable genes
Color Scale: Blue → White → Red (low → medium → high expression)

