import PyPDF2
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

uploadedFiles = []

# upload files
# there is a button to upload files. 
def uploadFiles(file):
    if file:
        file_path = file
        if file_path.endswith(".pdf"):
            uploadedFiles.append(file_path)
        else:
            print("Please select a valid PDF file to upload.")

def mergePDFs(output_file):
    merger = PyPDF2.PdfMerger()
    for pdf in uploadedFiles:
        merger.append(pdf)
    merger.write(output_file)
    merger.close()

# GUI

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("""
                           
            QWidget {
                font-family: Helvetica, sans-serif;
            }
            QPushButton {
                background-color: #CED3DC;
                color: black;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #BBBEC3;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        button_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.clicked.connect(self.uploadPDF)
        button_layout.addWidget(self.upload_button)

        self.clear_button = QPushButton("Clear PDFs")
        self.clear_button.clicked.connect(self.clearPDFs)
        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)

        self.file_list_widget = QListWidget()
        self.layout.addWidget(self.file_list_widget)

        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.mergePDFs)
        self.layout.addWidget(self.merge_button)

    def uploadPDF(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)", options=options)
        if file:
            uploadFiles(file)
            file_name = os.path.basename(file)
            self.file_list_widget.addItem(file_name)
        else:   
            QMessageBox.warning(self, "No File Selected", "Please select a PDF file to upload.")

    def mergePDFs(self):
        if uploadedFiles:
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
            if output_file:
                mergePDFs(output_file)
                QMessageBox.information(self, "Success", "PDFs merged successfully!")
        else:
            QMessageBox.warning(self, "No Files", "Please upload PDF files to merge.")

    def clearPDFs(self):
        uploadedFiles.clear()
        self.file_list_widget.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
