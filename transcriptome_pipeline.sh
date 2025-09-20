#!/bin/bash

# ======================= USER VARIABLES =======================
THREADS=$(nproc --ignore=2) # Automatically detect available threads (leaving 2 for system) 
SRA_ID="SRR32569850"
FASTA="sequences.fasta"
GTF="genome.gtf"
INDEX_PREFIX="${SRA_ID}_index"

# ======================= AUTO VARIABLES =======================
SRA_FILE="${SRA_ID}.sra"
FASTQ1="${SRA_ID}_1.fastq"
FASTQ2="${SRA_ID}_2.fastq"
TRIMMED1="${SRA_ID}_1.trimmed.fastq"
TRIMMED2="${SRA_ID}_2.trimmed.fastq"
FASTP_JSON="${SRA_ID}_fastp.json"
FASTP_HTML="${SRA_ID}_fastp.html"
BAM_FILE="${SRA_ID}_aln_sorted.bam"
COUNTS_OUTPUT="${SRA_ID}_featureCounts_output.txt"

# ======================= STEP 1: Fetch SRA =======================
#if [ ! -f "$SRA_FILE" ]; then
 #   echo "📥 Fetching $SRA_ID from SRA..."
  #  prefetch "$SRA_ID" || { echo "❌ Failed to fetch SRA data"; exit 1; }
#fi

# ======================= STEP 2: Convert to FASTQ =======================
if [ ! -f "$FASTQ1" ] || [ ! -f "$FASTQ2" ]; then
    echo "🔄 Converting SRA to FASTQ..."
    fasterq-dump "$SRA_ID" --split-files --threads "$THREADS" || { echo "❌ FASTQ conversion failed"; exit 1; }
fi

# ======================= STEP 3: Run fastp =======================
echo "🧪 Running fastp for QC and trimming..."
fastp -i "$FASTQ1" -I "$FASTQ2" \
      -o "$TRIMMED1" -O "$TRIMMED2" \
      --thread "$THREADS" \
      --json "$FASTP_JSON" --html "$FASTP_HTML" || { echo "❌ fastp failed"; exit 1; }

# ======================= STEP 4: Build index =======================
if [ ! -f "${INDEX_PREFIX}.files" ]; then
    echo "🔧 Building index..."
    subread-buildindex -o "$INDEX_PREFIX" "$FASTA" || { echo "❌ Index build failed"; exit 1; }
fi

# ======================= STEP 5: Alignment with Subjunc =======================
echo "🎯 Aligning reads with Subjunc..."
subjunc -i "$INDEX_PREFIX" \
        -r "$TRIMMED1" -R "$TRIMMED2" \
        -T "$THREADS" | \
    samtools view -@ "$THREADS" -bS - | \
    samtools sort -@ "$THREADS" -o "$BAM_FILE" || { echo "❌ Alignment failed"; exit 1; }

# ======================= STEP 6: featureCounts =======================
echo "📊 Running featureCounts..."
featureCounts -T "$THREADS" \
              -a "$GTF" \
              -o "$COUNTS_OUTPUT" \
              -t exon -g gene_id -p --primary \
              "$BAM_FILE" || { echo "❌ featureCounts failed"; exit 1; }

# ======================= DONE =======================
echo "✅ All steps completed successfully!"
echo "🔬 QC Report: $FASTP_HTML"
echo "📁 Counts: $COUNTS_OUTPUT"

