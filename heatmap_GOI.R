#heatmap for gene of intrest

#!/usr/bin/env Rscript

# ================================
# Automated Gene Heatmap Generator
# ================================
# This script:
# 1. Converts a .ods file to .csv using LibreOffice (headless mode)
# 2. Reads the FeatureCount CSV file
# 3. Extracts genes of interest
# 4. Performs log2 normalization
# 5. Generates a heatmap (PDF output)
# =================================

# Load required library
if(!require(pheatmap, quietly=TRUE)) {
  install.packages("pheatmap", repos = "https://cloud.r-project.org")
  library(pheatmap)
}

# ---------- USER VARIABLES ----------
input_file <- "Featurecount.ods"            # Input ODS file
output_csv <- "Featurecount.csv"            # Output CSV name
output_pdf <- "multi_gene_heatmap.pdf"      # Output PDF file
genes_of_interest <- c("WASH9P", "MIR12136", "OR4F16")
# ------------------------------------

# Convert ODS → CSV (headless)
cat("Converting ODS to CSV...\n")
system(paste("libreoffice --headless --convert-to csv", input_file, "--outdir ."))

# Check if conversion succeeded
if(!file.exists(output_csv)) {
  stop("CSV conversion failed. Check that LibreOffice is installed and accessible.")
}

cat("Reading CSV data...\n")
data <- read.csv(output_csv, header = TRUE, row.names = 1, skip = 1)

# Filter genes
cat("Filtering selected genes...\n")
gene_data <- data[genes_of_interest, , drop = FALSE]

# Check if genes exist
missing_genes <- setdiff(genes_of_interest, rownames(data))
if(length(missing_genes) > 0) {
  warning(paste("These genes were not found:", paste(missing_genes, collapse = ", ")))
}

# Log2 transform
cat("Applying log2 transformation...\n")
gene_data <- log2(as.matrix(gene_data) + 1)

# Generate heatmap
cat("Generating heatmap...\n")
pheatmap(gene_data,
         cluster_rows = FALSE,
         cluster_cols = FALSE,
         color = colorRampPalette(c("blue", "white", "red"))(50),
         fontsize_row = 10,
         fontsize_col = 10,
         main = "Expression of Selected Genes",
         filename = output_pdf)

cat(paste("✅ Heatmap saved to:", output_pdf, "\n"))
