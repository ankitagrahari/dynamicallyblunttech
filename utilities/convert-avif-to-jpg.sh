# Finds content folder, and then converts all avif images to jpg under images sub directory. 
find content -type f -path "*images*" | while read -r f; do
  if file -b "$f" | grep -q AVIF; then
    sips -s format jpeg "$f" --out "$f.tmp" && mv "$f.tmp" "$f" && echo "converted: $f"
  fi
done