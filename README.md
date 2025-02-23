# mergePDF

一个简单易用的PDF文件合并工具，基于PyQt6和PyPDF2开发，提供图形界面操作。

A user-friendly PDF file merger tool developed with PyQt6 and PyPDF2, featuring a graphical interface.

## 功能特性 | Features

- 支持多个PDF文件合并 | Support merging multiple PDF files
- 拖拽文件支持，方便添加PDF文件 | Drag and drop support for easy file addition
- 实时预览选中文件的页数信息 | Real-time preview of selected file page information
- 合并进度显示 | Merge progress display
- 按文件名排序 | Sort by filename
- 支持选择性删除文件 | Support selective file deletion

## 技术栈 | Tech Stack

- Python 3.x
- PyQt6 - GUI框架
- PyPDF2 - PDF处理库

## 安装依赖 | Installation

确保已安装Python 3.x，然后安装所需依赖：
Ensure Python 3.x is installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## 使用方法 | Usage

1. 运行程序 | Run the program:
   ```bash
   python main.py
   ```

2. 添加PDF文件 | Add PDF files:
   - 点击"Add Files"按钮选择文件 | Click "Add Files" button to select files
   - 或直接拖拽PDF文件到程序窗口 | Or drag and drop PDF files into the program window

3. 管理文件 | Manage files:
   - 在文件列表中选择文件可以预览文件信息 | Select files in the list to preview file information
   - 使用"Remove Selected"按钮删除不需要的文件 | Use "Remove Selected" button to delete unwanted files

4. 合并文件 | Merge files:
   - 确保已添加至少两个PDF文件 | Ensure at least two PDF files are added
   - 点击"Merge PDFs"按钮开始合并 | Click "Merge PDFs" button to start merging
   - 选择保存位置并等待合并完成 | Choose save location and wait for completion

## 贡献指南 | Contributing

欢迎贡献代码或提出建议！请遵循以下步骤：
Contributions are welcome! Please follow these steps:

1. Fork 项目 | Fork the project
2. 创建特性分支 | Create a feature branch
3. 提交更改 | Commit your changes
4. 推送到分支 | Push to the branch
5. 提交 Pull Request | Open a Pull Request

## 许可证 | License

本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解更多信息。
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
