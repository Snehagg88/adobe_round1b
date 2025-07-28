<!-- Objective
The goal of our solution is to build an intelligent document analyst that extracts and prioritizes relevant sections from a collection of diverse documents based on a specific persona and their job-to-be-done. The output follows a structured JSON format and captures metadata, extracted sections, and a refined analysis, all under resource and runtime constraints.

Input Format
The system takes the following input via a JSON file:

A list of documents (PDFs)

A persona: a role description with specific domain knowledge

A job-to-be-done: a specific task or objective that the persona wants to achieve

The documents are stored in a directory, and the paths are referenced in the JSON input.

Methodology
We used PyMuPDF (fitz) to parse and analyze PDFs due to its speed and support for lightweight extraction. Our logic focuses on keyword-based matching between the job description and document content.

For each document, we open and iterate through its pages.

Each page's text is scanned to see if any keyword from the job-to-be-done exists (case-insensitive match).

On the first relevant match:

We record the document name, page number, and a placeholder title.

We assign an importance_rank based on the order of relevance.

We also save the first 500 characters of text from that page for deeper analysis.

We break after the first match per document to save time and mimic a “first-relevant” prioritization approach.

Output Format
The output is a JSON file containing:

Metadata:

Input document names

Persona and job-to-be-done

Timestamp of processing

Extracted Sections:

Document name, section title, page number, and importance rank

Subsection Analysis:

Document name, page number, and a refined snippet of relevant text

Generalizability
This solution is domain-agnostic and works across academic, financial, educational, or business documents. By grounding the logic in job-specific keyword relevance, it adapts to different personas (students, analysts, researchers, etc.) and use cases without domain-specific tuning.

Constraints Handled
No internet access: The solution runs entirely offline.

≤ 1GB model size: No model is used; all logic is rule-based.

CPU-only: All processing uses lightweight CPU-compatible libraries.

≤ 60 seconds processing time: Early stopping and shallow parsing allow fast execution on 3–5 PDFs.

Limitations & Future Improvements
The current implementation uses exact keyword matching. This may miss semantically similar content.

Page-level granularity could be enhanced to section/subsection-level segmentation using font size, headings, or layout cues.

If allowed, integration with a small local language model could significantly improve semantic matching.
 -->


<!-- 2 -->


## Approach Explanation – Challenge 1B: Persona-Driven Document Intelligence

### Objective
Our system extracts and ranks relevant document sections based on a given persona and job-to-be-done. The system is designed to generalize across various domains and document types.

### 1. PDF Ingestion & Preprocessing
We used `PyMuPDF` to extract structured content (text, page numbers) from the PDFs. Each document was split into sections using heuristics based on headings (e.g., bold text, font size, line breaks).

### 2. Relevance Scoring
We use TF-IDF-based similarity scoring between section text and a combined persona + job-to-be-done prompt. This helps determine which sections are most relevant to the user's needs.

### 3. Section & Subsection Ranking
Sections are ranked using cosine similarity scores. Top N (e.g., 5) sections are selected, and within each, the most informative paragraph is selected for detailed subsection analysis.

### 4. Constraints Handling
- The entire pipeline runs under 60 seconds for 3–5 PDFs.
- Only lightweight libraries used (no internet access, total model/codebase size <1GB).
- Runs on CPU.

### Future Enhancements
- Incorporating layout analysis for better section boundary detection.
- Using compact sentence transformers (like MiniLM) if needed within size/time constraints.

