import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QListWidget,
                             QProgressBar, QFileDialog, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter

class PDFMerger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.resize(800, 500)
        self.files = []
        self.selected_items = set()

        self.init_ui()


    def init_ui(self):
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setAcceptDrops(True)  # 启用拖放
        self.file_list.dragEnterEvent = self.dragEnterEvent  # 处理拖拽进入事件
        self.file_list.dropEvent = self.dropEvent  # 处理拖放事件
        self.file_list.itemSelectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.file_list)

        # 按钮容器
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Files")
        remove_button = QPushButton("Remove Selected")
        merge_button = QPushButton("Merge PDFs")

        add_button.clicked.connect(self.add_files)
        remove_button.clicked.connect(self.remove_selected)
        merge_button.clicked.connect(self.merge_pdfs)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(merge_button)

        # 状态栏和进度条
        self.status_bar = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(button_layout)
        bottom_layout.addWidget(self.status_bar)
        bottom_layout.addWidget(self.progress_bar)
        left_layout.addLayout(bottom_layout)

        # 右侧预览面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        preview_title = QLabel("Preview")
        preview_title.setStyleSheet("font-weight: bold;")
        self.preview_label = QLabel("Select files to preview")
        self.preview_label.setWordWrap(True)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_layout.addWidget(preview_title)
        right_layout.addWidget(self.preview_label)

        # 添加面板到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.addWidget(splitter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.toLocalFile().lower().endswith('.pdf') for url in urls):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            pdf_files = [url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith('.pdf')]
            if pdf_files:
                self.files.extend(pdf_files)
                self.update_file_list()
                self.update_status()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF Files",
            "",
            "PDF Files (*.pdf)"
        )
        if files:
            self.files.extend(files)
            self.update_file_list()
            self.update_status()

    def update_file_list(self):
        self.file_list.clear()
        # 对文件列表进行排序
        self.files.sort(key=lambda x: os.path.basename(x).lower())
        for file in self.files:
            self.file_list.addItem(os.path.basename(file))

    def update_status(self):
        self.status_bar.setText(f"{len(self.files)} files selected")

    def on_selection_changed(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.preview_label.setText("Select files to preview")
            return

        preview_text = "Selected Files Preview\n" + "-" * 40 + "\n"
        total_pages = 0

        for item in selected_items:
            index = self.file_list.row(item)
            file_path = self.files[index]
            try:
                with open(file_path, 'rb') as file:
                    pdf = PdfReader(file)
                    pages = len(pdf.pages)
                    total_pages += pages
                    preview_text += f"📄 {os.path.basename(file_path)} ({pages} pages)\n"
            except Exception as e:
                preview_text += f"❌ {os.path.basename(file_path)} (Error: {str(e)})\n"

        preview_text += "-" * 40 + "\n"
        preview_text += f"Total Files: {len(selected_items)}\n"
        preview_text += f"Total Pages: {total_pages}"

        self.preview_label.setText(preview_text)

    def remove_selected(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return

        indices = [self.file_list.row(item) for item in selected_items]
        indices.sort(reverse=True)

        for index in indices:
            del self.files[index]

        self.update_file_list()
        self.update_status()
        self.preview_label.setText("Select files to preview")

    def merge_pdfs(self):
        if len(self.files) < 2:
            QMessageBox.information(self, "Notice", "Please select at least two PDF files to merge")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF",
            "merged.pdf",
            "PDF Files (*.pdf)"
        )

        if not output_file:
            return

        if not output_file.endswith('.pdf'):
            output_file += '.pdf'

        try:
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            self.status_bar.setText("Merging files...")

            merger = PdfWriter()
            total_pages = 0

            # 计算总页数
            for file_path in self.files:
                try:
                    with open(file_path, 'rb') as file:
                        pdf = PdfReader(file)
                        total_pages += len(pdf.pages)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to read PDF file: {os.path.basename(file_path)}\nError: {str(e)}")
                    self.status_bar.setText("Merge failed")
                    self.progress_bar.hide()
                    return

            current_page = 0
            # 合并文件
            for file_path in self.files:
                try:
                    with open(file_path, 'rb') as file:
                        pdf = PdfReader(file)
                        for page in pdf.pages:
                            merger.add_page(page)
                            current_page += 1
                            progress = int((current_page / total_pages) * 100)
                            self.progress_bar.setValue(progress)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to merge PDF file: {os.path.basename(file_path)}\nError: {str(e)}")
                    self.status_bar.setText("Merge failed")
                    self.progress_bar.hide()
                    return

            # 保存合并后的文件
            try:
                with open(output_file, 'wb') as output:
                    merger.write(output)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save merged PDF: {str(e)}")
                self.status_bar.setText("Merge failed")
                self.progress_bar.hide()
                return

            self.progress_bar.setValue(100)
            self.status_bar.setText("Merge completed")
            QMessageBox.information(
                self,
                "Success",
                f"PDF files merged successfully!\nMerged {len(self.files)} files, total {total_pages} pages"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to merge PDFs: {str(e)}")
            self.status_bar.setText("Merge failed")
        finally:
            self.progress_bar.hide()

def main():
    app = QApplication(sys.argv)
    merger = PDFMerger()
    merger.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()