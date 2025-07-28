# import os
# import json
# import datetime
# import fitz  # PyMuPDF

# # === CONFIGURATION ===
# collection = "collection_1"  # ✅ Use underscore to match actual folder name
# base_path = os.path.dirname(os.path.abspath(__file__))
# collection_path = os.path.join(base_path, collection)

# input_file = os.path.join(collection_path, "challenge1b_input.json")
# output_file = os.path.join(collection_path, "challenge1b_output.json")
# pdf_dir = os.path.join(collection_path, "PDFs")

# # === LOAD INPUT JSON ===
# with open(input_file, "r", encoding="utf-8") as f:
#     input_data = json.load(f)

# documents = input_data["documents"]
# persona = input_data["persona"]["role"]
# job = input_data["job_to_be_done"]["task"]

# # === PROCESS PDFs ===
# extracted_sections = []
# subsection_analysis = []

# for doc in documents:
#     filename = doc["filename"]
#     filepath = os.path.join(pdf_dir, filename)

#     try:
#         pdf = fitz.open(filepath)
#     except Exception as e:
#         print(f"❌ Could not open {filename}: {e}")
#         continue

#     for page_num, page in enumerate(pdf, start=1):
#         text = page.get_text()
#         if any(keyword.lower() in text.lower() for keyword in job.split()):
#             extracted_sections.append({
#                 "document": filename,
#                 "section_title": f"Relevant content on page {page_num}",
#                 "importance_rank": len(extracted_sections) + 1,
#                 "page_number": page_num
#             })
#             subsection_analysis.append({
#                 "document": filename,
#                 "refined_text": text[:500],  # First 500 characters
#                 "page_number": page_num
#             })
#             break  # only first matching page

# # === BUILD OUTPUT ===
# output_json = {
#     "metadata": {
#         "input_documents": [doc["filename"] for doc in documents],
#         "persona": persona,
#         "job_to_be_done": job,
#         "processing_timestamp": datetime.datetime.now().isoformat()
#     },
#     "extracted_sections": extracted_sections,
#     "subsection_analysis": subsection_analysis
# }

# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(output_json, f, indent=2)

# print("✅ Processing complete. Output saved to:", output_file)


# 2

# import os
# import json
# import datetime
# import fitz  # PyMuPDF
# # from transformers import pipeline

# def load_input(input_path):
#     with open(input_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def extract_section_title(text):
#     # Extract the first meaningful line as section title
#     for line in text.split("\n"):
#         cleaned = line.strip()
#         if 10 < len(cleaned) < 120:  # Adjustable threshold
#             return cleaned
#     return "Untitled Section"

# def extract_relevant_sections(documents, job_keywords, pdf_dir):
#     extracted_sections = []
#     subsection_analysis = []

#     importance_counter = 1  # Track rank

#     for doc in documents:
#         filename = doc["filename"]
#         filepath = os.path.join(pdf_dir, filename)

#         try:
#             pdf = fitz.open(filepath)
#         except Exception as e:
#             print(f"❌ Could not open {filename}: {e}")
#             continue

#         for page_num, page in enumerate(pdf, start=1):
#             text = page.get_text()

#             if any(kw.lower() in text.lower() for kw in job_keywords):
#                 section_title = extract_section_title(text)

#                 extracted_sections.append({
#                     "document": filename,
#                     "section_title": section_title,
#                     "importance_rank": importance_counter,
#                     "page_number": page_num
#                 })

#                 subsection_analysis.append({
#                     "document": filename,
#                     "refined_text": text[:500],
#                     "page_number": page_num
#                 })

#                 importance_counter += 1
#                 break  # Stop after first match per document

#     return extracted_sections, subsection_analysis

# def main():
#     # === CONFIGURATION ===
#     collection = "collection_1"
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     collection_path = os.path.join(base_path, collection)

#     input_file = os.path.join(collection_path, "challenge1b_input.json")
#     output_file = os.path.join(collection_path, "challenge1b_output.json")
#     pdf_dir = os.path.join(collection_path, "PDFs")

#     # === LOAD INPUT ===
#     input_data = load_input(input_file)
#     documents = input_data["documents"]
#     persona = input_data["persona"]["role"]
#     job = input_data["job_to_be_done"]["task"]
#     job_keywords = job.split()

#     # === PROCESS PDFs ===
#     extracted_sections, subsection_analysis = extract_relevant_sections(documents, job_keywords, pdf_dir)

#     # === BUILD OUTPUT ===
#     output_json = {
#         "metadata": {
#             "input_documents": [doc["filename"] for doc in documents],
#             "persona": persona,
#             "job_to_be_done": job,
#             "processing_timestamp": datetime.datetime.now().isoformat()
#         },
#         "extracted_sections": extracted_sections,
#         "subsection_analysis": subsection_analysis
#     }

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(output_json, f, indent=2)

#     print("✅ Processing complete. Output saved to:", output_file)

# if __name__ == "__main__":
#     main()


# 3
import os
import json
import fitz  # PyMuPDF
from datetime import datetime

# Input and output paths
input_file = "collection_1/challenge1b_input.json"
output_file = "collection_1/challenge1b_output.json"
pdf_dir = "collection_1/PDFs"

# Load input data
with open(input_file, "r", encoding="utf-8") as f:
    input_data = json.load(f)

persona = input_data["persona"]
job = input_data["job_to_be_done"]
input_documents = [doc["filename"] for doc in input_data["documents"]]


# Timestamp
timestamp = datetime.now().isoformat()

# Helper function to extract text from a specific page
def extract_text(pdf_path, page_number):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number - 1)
        text = page.get_text().strip()
        doc.close()
        return text
    except Exception as e:
        return f"Error reading page {page_number}: {str(e)}"

# Extraction logic
extracted_sections = []
subsection_analysis = []

importance = 1
for pdf_name in input_documents:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        section_title = page.get_text("text").split("\n")[0].strip() or "Introduction"
        refined_text = page.get_text("text").strip()

        extracted_sections.append({
            "document": pdf_name,
            "section_title": section_title,
            "importance_rank": importance,
            "page_number": 1
        })

        subsection_analysis.append({
            "document": pdf_name,
            "refined_text": refined_text,
            "page_number": 1
        })
        doc.close()
        importance += 1
    except Exception as e:
        print(f"Failed to process {pdf_name}: {e}")

# Final JSON structure
output_data = {
    "metadata": {
        "input_documents": input_documents,
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": timestamp
    },
    "extracted_sections": extracted_sections,
    "subsection_analysis": subsection_analysis
}

# Save output
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print(f"✅ Processing complete. Output saved to {output_file}")


# 4
