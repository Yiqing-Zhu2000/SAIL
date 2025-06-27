#!/bin/bash

INPUT=requirements.txt
OUTPUT=requirements_CC.txt

echo "# Auto-generated compatible requirements for Compute Canada" > "$OUTPUT"
echo "# Based on avail_wheels output" >> "$OUTPUT"
echo "" >> "$OUTPUT"

while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && echo "$line" >> "$OUTPUT" && continue

    # get package name（cut version info）
    pkg=$(echo "$line" | cut -d= -f1)

    # use avail_wheels extract package versions（except head line）
    pkg_lc=$(echo "$pkg" | tr '[:upper:]' '[:lower:]')
    available_versions=$(avail_wheels "$pkg" 2>/dev/null | tail -n +2 | awk -v p="$pkg" '$1 == p { print $2 }')

    if [[ -z "$available_versions" ]]; then
        echo "⚠️  $pkg not found in avail_wheels, keeping original line"
        echo "$line" >> "$OUTPUT"
        continue
    fi

    # select the last version
    best_version=$(echo "$available_versions" | sort -V | tail -n1)

    # write
    echo "$pkg==$best_version" >> "$OUTPUT"
    echo "✅ $pkg adjusted to version $best_version"

done < "$INPUT"

echo ""
echo "🎯 Done! Generated: $OUTPUT"
