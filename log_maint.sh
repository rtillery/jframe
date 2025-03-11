#!/bin/bash

MAX_SIZE=$((1024 * 1024)) # 1 MB in bytes

# Check if a log file is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi

LOG_FILE="$1"

# Check if the log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "[log_maint.sh] Log file does not exist: $LOG_FILE"
    exit 1
fi

# Get the size of the log file
FILE_SIZE=$(stat -c%s "$LOG_FILE")

# If the file size is greater than or equal to 1 MB
if [ "$FILE_SIZE" -ge "$MAX_SIZE" ]; then
    # Find the next available index for the compressed file
    INDEX=1
    while [ -f "${LOG_FILE}.${INDEX}.gz" ]; do
        INDEX=$((INDEX + 1))
    done

    # Compress the log file with the new index
    gzip -c "$LOG_FILE" > "${LOG_FILE}.${INDEX}.gz"

    # Clear the contents of the original log file
    > "$LOG_FILE"

    echo "[log_maint.sh] Log file compressed and cleared: ${LOG_FILE}.${INDEX}.gz"
else
    echo "[log_maint.sh] Log file size is under 1 MB: $FILE_SIZE bytes"
fi
