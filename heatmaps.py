#!/usr/bin/env python3
import subprocess
import sys
import os

if len(sys.argv) < 2:
    print("Usage: ./heatmaps.py <expression_matrix.(txt|csv|ods)>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "heatmap_output.pdf"
r_script = "heatmap_plot.R"

ext = os.path.splitext(input_file)[1].lower()

if ext == ".ods":
    r_code = f"""
if (!require("readODS", quietly=TRUE)) {{
    install.packages("readODS", repos="http://cran.us.r-project.org")
    library(readODS)
}}
if (!require("pheatmap", quietly=TRUE)) {{
    install.packages("pheatmap", repos="http://cran.us.r-project.org")
    library(pheatmap)
}}

data <- read_ods("{input_file}", 1)
rownames(data) <- data[,1]
data <- data[,-1]

data <- as.data.frame(lapply(data, as.numeric))
rownames(data) <- read_ods("{input_file}", 1)[,1]

data_log <- log2(data + 1)

# Select top 50 most variable genes
vars <- apply(data_log, 1, var)
top50 <- names(sort(vars, decreasing=TRUE))[1:50]
data_top <- data_log[top50, ]

conditions <- ifelse(grepl("Normal", colnames(data_top), ignore.case=TRUE), "Normal", "Diseased")
annotation <- data.frame(Condition = conditions)
rownames(annotation) <- colnames(data_top)

pheatmap(data_top,
         scale = "row",
         annotation_col = annotation,
         clustering_distance_rows = "euclidean",
         clustering_distance_cols = "euclidean",
         clustering_method = "complete",
         color = colorRampPalette(c("blue", "white", "red"))(50),
         fontsize_row = 6,
         filename = "{output_file}")
"""
elif ext == ".csv":
    r_code = f"""
if (!require("pheatmap", quietly=TRUE)) {{
    install.packages("pheatmap", repos="http://cran.us.r-project.org")
    library(pheatmap)
}}

data <- read.csv("{input_file}", header=TRUE, row.names=1, skip=1)
data <- as.data.frame(lapply(data, as.numeric))
rownames(data) <- rownames(read.csv("{input_file}", header=TRUE, row.names=1, skip=1))
data_log <- log2(data + 1)

# Top 50 variable genes
vars <- apply(data_log, 1, var)
top50 <- names(sort(vars, decreasing=TRUE))[1:50]
data_top <- data_log[top50, ]

pheatmap(data_top,
         scale = "row",
         clustering_distance_rows = "euclidean",
         clustering_distance_cols = "euclidean",
         clustering_method = "complete",
         color = colorRampPalette(c("blue", "white", "red"))(50),
         fontsize_row = 6,
         filename = "{output_file}")
"""
else:
    sep = "\\t"
    r_code = f"""
if (!require("pheatmap", quietly=TRUE)) {{
    install.packages("pheatmap", repos="http://cran.us.r-project.org")
    library(pheatmap)
}}

data <- read.table("{input_file}", header=TRUE, row.names=1, sep="{sep}", check.names=FALSE)
data <- as.data.frame(lapply(data, as.numeric))
rownames(data) <- rownames(read.table("{input_file}", header=TRUE, row.names=1, sep="{sep}", check.names=FALSE))
data_log <- log2(data + 1)

vars <- apply(data_log, 1, var)
top50 <- names(sort(vars, decreasing=TRUE))[1:50]
data_top <- data_log[top50, ]

pheatmap(data_top,
         scale = "row",
         clustering_distance_rows = "euclidean",
         clustering_distance_cols = "euclidean",
         clustering_method = "complete",
         color = colorRampPalette(c("blue", "white", "red"))(50),
         fontsize_row = 6,
         filename = "{output_file}")
"""

with open(r_script, "w") as f:
    f.write(r_code)

try:
    subprocess.run(["Rscript", r_script], check=True)
    print(f"✅ Heatmap saved to {output_file}")
except Exception as e:
    print("Error running R script:", e)
finally:
    if os.path.exists(r_script):
        os.remove(r_script)

