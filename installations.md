🧰 Input Requirements:                                                            
| File       | Description               | Example           |                        
| ---------- | ------------------------- | ----------------- |
| **FASTA**  | Reference genome sequence | `sequences.fasta` |
| **GTF**    | Genome annotation file    | `genome.gtf`      |
| **SRA ID** | Accession from NCBI SRA   | `SRR********`     |

Install Conda and check version
```bash
conda --version 
```
Create an conda environment
```bash
conda create -n rnaseq python=3.10 -y
conda activate rnaseq
```
Configure Bioconda channels
```bash
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```
Install all required tools - fasterq-dump | fastp | subread-buildindex | subjunc | featureCounts | samtools
```bash
conda install sra-tools fastp subread samtools -y
```
Verify installation
```bash
samtools --version
fastp --version
subjunc -h
featureCounts -h
fasterq-dump --version
```
Prepare your working directory
```bash
mkdir rnaseq_project
cd rnaseq_project
```
Make script executable
```bash
chmod +x script.sh
```
Run the pipeline
```bash
./script.sh
```
📁 Output Files:
| Output File                              | Description              |
| ---------------------------------------- | ------------------------ |
| `*_1.trimmed.fastq`, `*_2.trimmed.fastq` | Trimmed paired-end reads |
| `*_fastp.html`, `*_fastp.json`           | Quality reports          |
| `*_index.*`                              | Genome index files       |
| `*_aln_sorted.bam`                       | Sorted BAM alignment     |
| `*_featureCounts_output.txt`             | Gene-level read counts   |
```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```


