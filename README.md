# stringextractor
File Analyzer is a Python tool for binary file analysis. It extracts strings and URLs, calculates SHA-256 hashes, and visualizes string length distributions. With a user-friendly GUI, it generates HTML reports for easy interpretation. Ideal for malware analysis, forensics, and general file inspection tasks.




# File Analyzer

File Analyzer is a Python application that provides detailed analysis of binary files, extracting strings, URLs, and generating visual representations of the file contents.

## Features

- File selection via GUI
- SHA-256 hash calculation
- Extraction of printable ASCII strings
- Detection of HTTPS URLs
- Generation of string length distribution histogram
- Creation of an HTML report with all findings

## Requirements

- Python 3.x
- tkinter
- matplotlib
- chardet

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/file-analyzer.git
   ```

2. Navigate to the project directory:
   ```
   cd file-analyzer
   ```

3. Install the required packages:
   ```
   pip install matplotlib chardet
   ```

## Usage

1. Run the script:
   ```
   python file_analyzer.py
   ```

2. Click the "Analyze File" button in the GUI.

3. Select the file you want to analyze.

4. Wait for the analysis to complete. A progress bar will show the current status.

5. Once complete, an HTML report will be generated in the same directory as the analyzed file.

## Output

The HTML report includes:

- File metadata (name, size, SHA-256 hash)
- A histogram showing the distribution of string lengths
- The first 1000 extracted strings
- All detected HTTPS URLs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

