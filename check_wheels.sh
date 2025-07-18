#!/bin/bash

# pay attention : avail_wheels --all torch
# This would see all versions of torch, but here I didn't use it
# here I just check "there is a package exists in CC"

REQ_FILE="requirements.txt"

echo "🧪 Checking available wheels from Compute Canada for each package in $REQ_FILE"
echo "------------------------------------------------------------"
module load python/3.10 

while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue

    # get package name（but cut the version info and = ）
    pkg=$(echo "$line" | cut -d= -f1)

    echo -n "🔍 $pkg ... "

    if avail_wheels "$pkg" &> /dev/null; then
        echo "✅ available"
    else
        echo "❌ NOT available"
    fi

done < "$REQ_FILE"

echo "------------------------------------------------------------"
echo "✅ Done."
