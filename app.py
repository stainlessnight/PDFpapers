import streamlit as st
import os
import subprocess

def extract_with_nougat(pdf_path, output_dir):
    """Nougatを使用してPDFから.mmd形式のテキストを抽出する関数"""
    cmd = ["nougat", pdf_path, "-o", output_dir]
    subprocess.run(cmd)
    mmd_file_path = os.path.join(output_dir, os.path.basename(pdf_path).replace('.pdf', '.mmd'))
    with open(mmd_file_path, 'r') as f:
        content = f.read()
    return content, mmd_file_path

def read_mmd(mmd_path):
    """直接.mmdファイルを読み込む関数"""
    with open(mmd_path, 'r') as f:
        return f.read()

def render_mathpix_markdown(mmd_content):
    """Mathpix Markdownの内容をStreamlitでレンダリングする"""
    html_code = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.2/katex.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.2/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mathpix-markdown-it@1.0.40/es5/bundle.js"></script>
    <div id="math-content">
        {mmd_content}
    </div>
    <script>
        window.onload = function () {{
            const options = {{
                output: 'html',
                decimalMark: 'auto',
                minRuleThickness: 0.05,
                macros: {{}},
                strict: 'warn',
                trust: false
            }};
            const htmlElement = document.getElementById('math-content');
            window.renderMathInElement(htmlElement, options);
        }};
    </script>
    """
    st.components.v1.html(html_code, height=600, scrolling=True)


st.title("PDF/.mmdからMathpix Markdown形式の数式抽出アプリ")

uploaded_file = st.file_uploader("PDFファイルまたは.mmdファイルをアップロードしてください", type=["pdf", "mmd"])

if uploaded_file:
    if uploaded_file.name.endswith('.pdf'):
        pdf_temp_path = os.path.join(".", uploaded_file.name)
        with open(pdf_temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        latex_output, mmd_path = extract_with_nougat(pdf_temp_path, ".")
    elif uploaded_file.name.endswith('.mmd'):
        with open("temp.mmd", "wb") as f:
            f.write(uploaded_file.getbuffer())
        latex_output = read_mmd("temp.mmd")
    render_mathpix_markdown(latex_output)
    # st.markdown(latex_output)
