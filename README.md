# 📚 AI-Powered PDF Book Generator

An intelligent curriculum generator that creates comprehensive, professionally formatted PDF books using OpenAI's GPT-4o-mini. Perfect for generating educational content, technical documentation, and training materials with minimal effort.

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Hierarchical Structure**: Automatically breaks down topics into modules → submodules → sub-submodules
- **Comprehensive Content**: Generates theory, code examples, exercises, and quizzes
- **Beginner-Friendly Tone**: Conversational, encouraging content written for first-time learners
- **Smart Context**: Uses AI to create relevant, educational content tailored to your topic

### 📄 Professional PDF Output
- **Beautiful Typography**: Custom styles, colors, and professional formatting
- **Code Blocks**: Syntax-highlighted code with proper indentation and background styling
- **Tables**: Professional tables with headers, alternating row colors, and borders
- **Key Takeaways**: Highlighted boxes with important points
- **Quiz Section**: Comprehensive quiz with questions, options, answers, and explanations
- **Page Management**: Smart page breaks and `KeepTogether` to prevent content splitting

### 📊 Multiple Output Formats
- **PDF Book**: Professional, print-ready PDF
- **Text File**: Human-readable curriculum outline
- **JSON File**: Structured data for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API Key
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/7plutus7/Content-Generator.git
cd Content-Generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Usage

Run the generator:
```bash
python notes_generator.py
```

The script will:
1. Generate hierarchical curriculum structure
2. Create detailed content for each topic
3. Generate a comprehensive quiz
4. Build a professional PDF book
5. Save text and JSON backups

## 📁 Output Files

After running, you'll get:

- `python_data_for_ai_book.pdf` - Professional PDF book (30-40 pages)
- `python_data_for_ai_curriculum.txt` - Formatted text outline
- `python_data_for_ai_curriculum.json` - Structured JSON data

## 🎨 Customization

### Modify Course Topic

Edit the `specs` list in the `build_course()` function:

```python
specs = [
    ("Your Module Name", "Guidance for content generation"),
    ("Another Module", "Focus on specific aspects..."),
    # Add more modules...
]
```

### Adjust PDF Styling

Customize styles in the `generate_pdf_book()` function:

```python
heading_style = ParagraphStyle(
    'CustomHeading',
    fontSize=16,
    textColor=colors.HexColor('#YOUR_COLOR'),
    # ... more customization
)
```

### Change Content Depth

Modify the module structure generation in `generate_module_structure()`:

```python
f"1. Break this module into 3-5 SUBMODULES\n"  # Adjust numbers here
f"2. For each submodule, identify 2-4 SUB-SUBMODULES\n"  # Adjust here
```

## 📋 Course Structure

The default course generates content for:

1. **Python Basics & Environment Setup** - Installation, IDEs, first programs
2. **Variables, Data Types & Operators** - Fundamentals of Python programming
3. **Control Flow & Functions** - Logic and code organization
4. **Numpy Arrays for AI** - Numerical computing essentials
5. **Pandas for Data** - Data manipulation and analysis
6. **Matplotlib for Visualization** - Creating charts and graphs

## 💰 Cost Estimation

- **Estimated Time**: 10-15 minutes per run
- **Estimated Cost**: $0.10-$0.15 (using GPT-4o-mini)
- **Output**: ~30-40 pages of professional content

## 🛠️ Technical Stack

- **OpenAI GPT-4o-mini**: Content generation
- **ReportLab**: PDF creation and styling
- **Python-dotenv**: Environment variable management

## 📖 Example Output Structure

```
📘 Python & Data for AI

Chapter 1: Python Basics
├── 1.1 Installation & Setup
│   ├── 1.1.1 Installing Python
│   │   • Theory
│   │   • Code Examples
│   │   • Key Takeaways
│   ├── 1.1.2 Setting Up IDE
│   └── ...
├── 1.2 First Programs
└── ...

Chapter 2: Variables & Data Types
...

📝 Comprehensive Quiz
Q1. What is a variable in Python?
A. A container for data
B. A type of loop
C. A function
D. A module
✓ Answer: A - A variable is a container...
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Model Configuration

The script uses `gpt-4o-mini` by default. You can change this in the code:

```python
model="gpt-4o-mini",  # Change to gpt-4, gpt-3.5-turbo, etc.
temperature=0.4,       # Adjust creativity (0.0-1.0)
max_tokens=2000        # Adjust response length
```

## 🔧 Troubleshooting

### Common Issues

**Issue**: `openai.AuthenticationError`
- **Solution**: Check your `.env` file and ensure `OPENAI_API_KEY` is correct

**Issue**: PDF doesn't generate
- **Solution**: Ensure ReportLab is installed: `pip install reportlab`

**Issue**: Content generation fails
- **Solution**: Check your OpenAI API credits and internet connection

**Issue**: Code blocks missing indentation
- **Solution**: Already fixed! Uses `&nbsp;` for proper spacing

**Issue**: Quiz not in PDF
- **Solution**: Already fixed! Quiz appears at the end of the PDF

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation


## 👨‍💻 Author

Created by [7plutus7](https://github.com/7plutus7)

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- ReportLab for PDF generation capabilities
- The Python community for excellent libraries

