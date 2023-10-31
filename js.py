import streamlit as st

def main():
    mmd = """
    This is a sample markdown text with a math equation:
    $$ E = mc^2 $$
    """
    
    # JavaScriptの埋め込み
    js_code = f"""
        <script>
            let script = document.createElement('script');
            script.src = "https://cdn.jsdelivr.net/npm/mathpix-markdown-it@1.0.40/es5/bundle.js";
            document.head.append(script);

            script.onload = function() {{
                const isLoaded = window.loadMathJax();
                if (isLoaded) {{
                    console.log('Styles loaded!')
                    // When the library is loaded, render the markdown text
                    let content = document.getElementById('mmd-content');
                    content.innerHTML = window.markdownit().render({mmd});
                }}
            }}
        </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
    st.markdown('<div id="mmd-content"></div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
