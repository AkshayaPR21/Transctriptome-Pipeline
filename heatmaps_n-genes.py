#!/usr/bin/env python3
import subprocess
import sys
import os
import tempfile

# ===============================
# ✅  Usage: ./heatmaps.py <expression_matrix.(txt|csv|ods)> [top_n]
# ./heatmaps.py featurecounts.ods 25
# ===============================

if len(sys.argv) < 2:
    print("Usage: ./heatmaps.py <expression_matrix.(txt|csv|ods)> [top_n]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "heatmap_output.pdf"
top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 50  # default top 50 genes

# -------------------------------
# Detect file extension
# -------------------------------
ext = os.path.splitext(input_file)[1].lower()

# Temporary R script
r_script_path = tempfile.mktemp(suffix=".R")

# -------------------------------
# Generate R script dynamically
# -------------------------------
r_code = f"""
if (!require("pheatmap", quietly=TRUE)) {{
    install.packages("pheatmap", repos="http://cran.us.r-project.org")
    library(pheatmap)
}}

# Helper function to clean and normalize data
clean_data <- function(df) {{
    df <- as.data.frame(df)
    df <- df[, colSums(is.na(df)) < nrow(df)]  # remove empty cols
    gene_col <- df[, 1]
    df <- df[, -1, drop=FALSE]
    df[] <- lapply(df, function(x) as.numeric(as.character(x)))
    rownames(df) <- make.names(gene_col, unique=TRUE)
    df <- df[rowSums(is.na(df)) < ncol(df), ]
    return(df)
}}

# Load file based on extension
ext <- tools::file_ext("{input_file}")
if (ext == "csv") {{
    data_raw <- read.csv("{input_file}", header=TRUE, sep=",", check.names=FALSE)
    data <- clean_data(data_raw)
}} else if (ext == "txt" || ext == "tsv") {{
    data_raw <- read.delim("{input_file}", header=TRUE, sep="\\t", check.names=FALSE)
    data <- clean_data(data_raw)
}} else if (ext == "ods") {{
    if (!require("readODS", quietly=TRUE)) {{
        install.packages("readODS", repos="http://cran.us.r-project.org")
        library(readODS)
    }}
    data_raw <- read_ods("{input_file}", 1)
    data <- clean_data(data_raw)
}} else {{
    stop("Unsupported file type. Please provide .csv, .txt, or .ods")
}}

# Log2 transform
data_log <- log2(data + 1)

# Select top variable genes
vars <- apply(data_log, 1, var, na.rm=TRUE)
top_genes <- names(sort(vars, decreasing=TRUE))[1:{top_n}]
data_top <- data_log[top_genes, , drop=FALSE]

# Generate heatmap
pheatmap(data_top,
         scale="row",
         clustering_distance_rows="euclidean",
         clustering_distance_cols="euclidean",
         clustering_method="complete",
         color=colorRampPalette(c("blue", "white", "red"))(50),
         fontsize_row=6,
         filename="{output_file}")
cat("✅ Heatmap successfully saved as {output_file}\\n")
"""

# -------------------------------
# Write and execute R script
# -------------------------------
with open(r_script_path, "w") as f:
    f.write(r_code)

try:
    subprocess.run(["Rscript", r_script_path], check=True)
finally:
    os.remove(r_script_path)
