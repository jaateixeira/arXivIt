
# arXivIt
Pre-processes latex working papers for archival at arXiv.org


**arXivIt** is a script designed to prepare your LaTeX project for submission to arXiv. It automates the process of validating, cleaning, and packaging your project into a `.tar` file that complies with arXiv's strict requirements. This manual explains how to use arXivIt and what it does.



## **Features**
arXivIt performs the following tasks to ensure your LaTeX project is ready for arXiv submission:

1. **Validates Sources**:
   - Ensures your project contains valid (La)TeX, AMS(La)TeX, or PDFLaTeX sources.

2. **Validates Figures**:
   - Ensures figures are in valid formats: PostScript (PS, EPS), JPEG, GIF, PNG, or PDF.

3. **Flattens Main `.tex` File**:
   - Combines all `\input` and `\include` statements into a single, flattened `.tex` file.

4. **Checks Filenames**:
   - Ensures filenames comply with arXiv's strict requirements (e.g., no spaces, special characters, or overly long names).

5. **Removes Unused Files**:
   - Deletes any files not referenced by your main `.tex` file.

6. **Handles Symlinks**:
   - Replaces symbolic links with hard copies of the files.

7. **Removes Conflicting PDFs**:
   - Deletes any `.pdf` files that might conflict with arXiv's processing.

8. **Cleans Hidden Files**:
   - Deletes hidden files and directories (e.g., `.gitignore`, `.DS_Store`).

9. **Warns About Empty Files**:
   - Alerts you if any files in your project are empty.

10. **Validates `.bbl` File**:
    - Ensures the `.bbl` file matches the name of the main `.tex` file for proper reference processing.

---

## **Usage**

### **Input**
- A folder containing your LaTeX project. The folder must include:
  - A main `.tex` file (e.g., `main.tex`).
  - Any additional `.tex` files, figures, and references.

### **Output**
- A `.tar` file ready for upload to arXiv.

---

## **How to Run arXivIt**

### **Prerequisites**
- Ensure you have Python 3 installed.
- Install required Python packages (if any) using `pip install -r requirements.txt`.

### **Running the Script**
1. Place your LaTeX project in a folder (e.g., `my_latex_project`).
2. Run the script from the command line:
   ```bash
   python arxivit.py /path/to/my_latex_project