import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import hashlib
import matplotlib.pyplot as plt
import io
import base64
import re
import os
import html
import traceback
import chardet

def extract_strings_and_urls(content):
    try:
        # Extract printable ASCII strings
        ascii_strings = re.findall(b'[ -~]{4,}', content)
        strings = [s.decode('ascii', errors='replace') for s in ascii_strings]
        
        # Extract URLs starting with https
        https_urls = re.findall(b'https://[^\s\'"]+', content)
        urls = [u.decode('ascii', errors='replace') for u in https_urls]
        
        return strings, urls
    except Exception:
        return [], []

def analyze_file():
    try:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        progress_window = tk.Toplevel(root)
        progress_window.title("Analyzing File")
        progress_window.geometry("300x100")
        
        progress_label = tk.Label(progress_window, text="Analyzing...")
        progress_label.pack(pady=10)
        
        progress_bar = Progressbar(progress_window, length=200, mode='determinate')
        progress_bar.pack(pady=10)

        file_size = os.path.getsize(file_path)
        
        progress_label.config(text="Reading file...")
        progress_window.update()

        with open(file_path, 'rb') as file:
            content = file.read()

        progress_bar['value'] = 20
        progress_window.update()

        file_hash = hashlib.sha256(content).hexdigest()

        progress_label.config(text="Extracting strings and URLs...")
        progress_window.update()

        all_strings, https_urls = extract_strings_and_urls(content)

        progress_bar['value'] = 60
        progress_label.config(text="Generating graph...")
        progress_window.update()

        # Create histogram of string lengths
        string_lengths = [len(s) for s in all_strings]
        plt.figure(figsize=(10, 5))
        plt.hist(string_lengths, bins=50, edgecolor='black')
        plt.title('Distribution of String Lengths')
        plt.xlabel('String Length')
        plt.ylabel('Frequency')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        progress_bar['value'] = 80
        progress_label.config(text="Generating HTML report...")
        progress_window.update()

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                .list-container {{ max-height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>File Analysis Report for: {html.escape(os.path.basename(file_path))}</h1>
            <p><strong>SHA-256 Hash:</strong> {file_hash}</p>
            <p><strong>File Size:</strong> {file_size:,} bytes</p>
            
            <h2>Distribution of String Lengths:</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Distribution of String Lengths">
            
            <h2>Extracted Strings (first 1000):</h2>
            <div class="list-container">
                <ol>
                    {"".join(f"<li>{html.escape(str(string))}</li>" for string in all_strings[:1000])}
                </ol>
            </div>
            <p>Showing first 1000 strings (if more than 1000 were found).</p>

            <h2>HTTPS URLs:</h2>
            <div class="list-container">
                <ul>
                    {"".join(f"<li><a href='{url}'>{html.escape(url)}</a></li>" for url in https_urls)}
                </ul>
            </div>
        </body>
        </html>
        """

        html_path = os.path.splitext(file_path)[0] + '_analysis.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        progress_bar['value'] = 100
        progress_window.destroy()
        print(f"Analysis complete. HTML report saved as: {html_path}")
        messagebox.showinfo("Analysis Complete", f"HTML report saved as:\n{html_path}")

    except Exception as e:
        error_msg = f"An error occurred:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        messagebox.showerror("Error", error_msg)

root = tk.Tk()
root.title("File Analyzer")
root.geometry("300x100")

analyze_button = tk.Button(root, text="Analyze File", command=analyze_file)
analyze_button.pack(expand=True)

root.mainloop()