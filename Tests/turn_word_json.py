from docx import Document
import pandas as pd
import os
# Use a raw string (prefix with r) to prevent backslash issues
doc_path = r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\Tests\calc_documentation.docx'
json_path = r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\Tests\paragraph_chunks.json'

# Load the document
doc = Document(doc_path)

# Extract non-empty paragraph chunks
paragraph_chunks = [para.text.strip() for para in doc.paragraphs if para.text.strip() != ""]


# Save the chunks to a JSON file
df = pd.DataFrame({
    "id": range(len(paragraph_chunks)),
    "text": paragraph_chunks
})

df.to_json(json_path, orient='records', lines=True)

