awk '(NR == 1) || (FNR > 1)' course_*.tsv > new_merged_file.tsv

cut -f12 new_merged_file.tsv | sort | uniq -c | sort -nr

cut -f11 new_merged_file.tsv | sort | uniq -c | sort -nr

awk -F'\t' '$5=="False" {count++} END {print count}' new_merged_file.tsv

total_courses=$(awk -F'\t' 'NR>1' new_merged_file.tsv | wc -l)
engineering_courses=$(awk -F'\t' 'NR>1 && tolower($4) ~ /engineer/' new_merged_file.tsv | wc -l)
percentage=$(echo "$engineering_courses * 100 / $total_courses" | bc -l)
echo $percentage
