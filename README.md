# 🍔 Smart Menu Intelligence (RAG Pipeline)

A "Menu RAG" system that digitizes unstructured restaurant data (images) into a structured, searchable AI database.

## 🚀 The Problem
Local businesses (any Bakery) often share menus as **Unstructured Data** (JPG images) on social media.
* **Searchability:** Zero. You cannot Ctrl+F an image.
* **Accessibility:** Users cannot filter by budget or dietary preference.
* **UX:** Customers have to scroll through dozens of photos to find prices.

## 🛠️ The Solution
I built an end-to-end AI pipeline that:
1.  **Extracts** raw text from images using Computer Vision.
2.  **Cleans** and structures the data using Large Language Models (LLMs).
3.  **Serves** the data via a Natural Language Chat Interface.

## ⚙️ Technical Architecture

### 1. Data Ingestion (OCR Layer)
* **Tool:** `EasyOCR` (Python)
* **Function:** Converts pixel data from menu images into raw text lines.
* **Challenge Solved:** Handled complex layouts and non-standard fonts used in bakery graphic design.

### 2. Data Cleaning (LLM Layer)
* **Tool:** Google Gemini 1.5 Flash (via API)
* **Function:** Takes the "dirty" OCR text (e.g., `Eggs Bonedicl`) and uses semantic understanding to correct it to `Eggs Benedict`.
* **Normalization:** Converted mixed price formats (e.g., `500rs`, `500/-`) into pure Float/Integer values for mathematical filtering.

>
### 3. The "Brain" (Retrieval Logic)
* **Fuzzy Matching:** implemented `difflib` to handle user typos (e.g., matching "borgir" to "Burger").
* **Intent Classification:** The system detects if a query is **Navigational** ("Show menu") or **Transactional** ("Under 500 rupees") and switches search logic accordingly.

.

## 💻 How to Run Locally

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/smart-menu-rag.git](https://github.com/YOUR_USERNAME/smart-menu-rag.git)
