for file in *.md; do
    pandoc "$file" -o "${file%.md}.docx"
done
