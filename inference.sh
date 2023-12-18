#!/bin/bash

Check if a text file is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <text_file>"
  exit 1
fi

text_file="$1"

# Check if the provided text file exists
if [ ! -f "$text_file" ]; then
  echo "Error: Text file '$text_file' not found."
  exit 1
fi
# Define the list of speaker IDs
speakers="92 6097 6670 6671 8051 9017 9136 11614 11697 12787"
counter=1

# Read lines from text_file.txt
while IFS= read -r line; do
  # Skip empty lines
  [ -z "$line" ] && continue

  label="text$counter"
  counter=$((counter+1))

    # Iterate through each fixed speaker ID
    for speaker_id in $speakers; do
    output_dir="/mnt/workspace/tzeying/inference/inf_librihifi_320k/trial1/${label}/${speaker_id}"
    speaker_name="hifitts_${speaker_id}"

    sh /mnt/workspace/wangmingxuan/vits_on_libritts_hifitts/Amphion/egs/tts/vits_hifitts/run.sh \
        --stage 3 \
        --gpu "4" \
        --infer_expt_dir /mnt/workspace/xueliumeng/data/vits_on_libritts_hifitts/logs/Libri_HifiTTS_All \
        --infer_output_dir "$output_dir" \
        --infer_mode "single" \
        --infer_text "$line" \
        --infer_speaker_name "$speaker_name"

    echo "Processing complete for speaker ID: $speaker_id"
    done
  echo "Processing complete for line: $counter"
done < "$text_file"
