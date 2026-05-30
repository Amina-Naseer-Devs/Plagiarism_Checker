import streamlit as st
import pandas as pd
import os
from similarity import check_similarity, get_warning, get_top_match
from preprocessing import word_count

# ── PAGE CONFIGURATION ────────────────────────────────
st.set_page_config(
    page_title="Content Similarity Detector",
    page_icon="🔍",
    layout="centered"
)

# ── CUSTOM CSS ────────────────────────────────────────
st.markdown("""
    <style>
        .main-header {
            font-size: 2rem;
            font-weight: 700;
            color: #1f77b4;
            text-align: center;
        }
        .sub-header {
            font-size: 1rem;
            color: #555555;
            text-align: center;
            margin-bottom: 30px;
        }
        .result-box {
            background-color: #f0f4f8;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .top-match {
            font-size: 1.1rem;
            font-weight: 600;
            color: #d62728;
        }
    </style>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 About This Project")
    st.write("""
        A Content Similarity Detection System
        built using NLP techniques to support
        intellectual property protection.
    """)

    st.divider()

    st.markdown("### ⚙️ Technology Stack")
    st.markdown("""
        - **Language:** Python  
        - **NLP:** TF-IDF Vectorization  
        - **Similarity:** Cosine Similarity  
        - **UI:** Streamlit  
        - **Library:** scikit-learn  
    """)

    st.divider()

    st.markdown("### 📁 Reference Corpus")
    data_path = "data"
    if os.path.exists(data_path):
        doc_count = len([f for f in os.listdir(data_path)
                         if f.endswith(".txt")])
        st.metric(label="Documents Loaded", value=doc_count)
    else:
        st.warning("No /data folder found.")

    st.divider()

    st.markdown("### 🚦 Similarity Scale")
    st.markdown("""
        - 🔴 **70%+** → High Similarity
        - 🟡 **40–69%** → Moderate Similarity  
        - 🟢 **0–39%** → Low Similarity  
    """)

    st.divider()
    st.caption("Built for academic & IP research purposes")
    st.caption("Inspired by digital content attribution challenges")


# ── HEADER ────────────────────────────────────────────
st.markdown('<div class="main-header">🔍 Content Similarity Detector</div>',
            unsafe_allow_html=True)

st.markdown('<div class="sub-header">Detect potential copyright violations using NLP</div>',
            unsafe_allow_html=True)

st.divider()


# ── ABOUT SECTION ─────────────────────────────────────
with st.expander("ℹ️ About This Tool"):
    st.write("""
        This tool compares your text against a reference corpus to detect
        content similarity. It uses **TF-IDF Vectorization** and
        **Cosine Similarity** to calculate how closely your content
        matches existing documents.

        - 🔴 Above 70% similarity → Potential copyright concern
        - 🟡 40% to 70% similarity → Review recommended
        - 🟢 Below 40% similarity → Content appears original
    """)

st.divider()


# ── WELCOME MESSAGE ───────────────────────────────────
st.markdown("""
    <div style="
        background-color: #e8f4fd;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 20px;
    ">
        <strong>👋 How to use this tool:</strong><br>
        Paste your text or upload a .txt file below,
        then click <strong>Analyze Content</strong> to check
        for similarity against our reference corpus.
    </div>
""", unsafe_allow_html=True)


# ── INPUT METHOD SELECTOR ─────────────────────────────
st.markdown("### 📥 Choose Input Method")

input_method = st.radio(
    label="How would you like to provide content?",
    options=["✍️ Paste Text", "📂 Upload .txt File"],
    horizontal=True
)

st.divider()


# ── INPUT SECTION ─────────────────────────────────────
input_text = ""

if input_method == "✍️ Paste Text":
    st.markdown("### 📝 Enter Your Content")
    input_text = st.text_area(
        label="Paste your text below:",
        placeholder="Paste your article, blog post, or product description here...",
        height=200
    )
    if input_text:
        st.caption(f"Word count: {word_count(input_text)}")

elif input_method == "📂 Upload .txt File":
    st.markdown("### 📂 Upload Your File")
    uploaded_file = st.file_uploader(
        label="Upload a .txt file:",
        type=["txt"]
    )
    if uploaded_file is not None:
        input_text = uploaded_file.read().decode("utf-8")
        st.markdown("**📄 File Preview:**")
        st.text_area(
            label="File contents:",
            value=input_text,
            height=200,
            disabled=True
        )
        st.caption(f"File: {uploaded_file.name}  |  "
                   f"Word count: {word_count(input_text)}")
    else:
        st.info("👆 Please upload a .txt file to continue.")

st.divider()


# ── BUTTONS ───────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    analyze = st.button("🔍 Analyze Content", use_container_width=True)
with col2:
    clear = st.button("🗑️ Clear", use_container_width=True)

if clear:
    st.rerun()


# ── RESULTS SECTION ───────────────────────────────────
if analyze:

    if not input_text or not input_text.strip():
        st.error("⛔ Please enter or upload some text before analyzing.")

    else:
        status, results = check_similarity(input_text)

        if status == "too_short":
            st.error("⛔ Text is too short. Please enter at least 3 words.")

        elif status == "invalid_content":
            st.error("⛔ No valid content detected. Please enter real text.")

        elif status == "no_documents":
            st.error("⛔ No reference documents found. "
                     "Please check the /data folder.")

        elif status == "success":

            # ── SUMMARY STATS ──────────────────────────
            st.markdown("### 📈 Analysis Summary")

            total_docs = len(results)
            high_risk  = len([r for r in results if r[1] >= 70])
            moderate   = len([r for r in results if 40 <= r[1] < 70])
            low_risk   = len([r for r in results if r[1] < 40])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="📄 Docs Checked", value=total_docs)
            with col2:
                st.metric(label="🔴 High Risk", value=high_risk)
            with col3:
                st.metric(label="🟡 Moderate", value=moderate)
            with col4:
                st.metric(label="🟢 Low Risk", value=low_risk)

            st.divider()

            # ── RESULTS TABLE ──────────────────────────
            st.markdown("### 📊 Similarity Results")

            df = pd.DataFrame(results, columns=["Document", "Similarity (%)"])
            df.index = df.index + 1

            def color_score(val):
                if val >= 70:
                    return 'background-color: #ffcccc'
                elif val >= 40:
                    return 'background-color: #fff3cc'
                else:
                    return 'background-color: #ccffcc'

            styled_df = df.style.map(
                color_score, subset=["Similarity (%)"]
            )
            st.dataframe(styled_df, use_container_width=True)

            st.divider()

            # ── TOP MATCH ──────────────────────────────
            st.markdown("### 🎯 Top Match")

            top_doc, top_score = get_top_match(results)

            st.markdown(f"""
                <div class="result-box">
                    <p class="top-match">📄 {top_doc}</p>
                    <p>Similarity Score: <strong>{top_score}%</strong></p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("**Similarity Level:**")
            st.progress(int(top_score))

            if top_score >= 70:
                st.caption("🔴 High similarity detected")
            elif top_score >= 40:
                st.caption("🟡 Moderate similarity detected")
            else:
                st.caption("🟢 Low similarity — content appears original")

            st.divider()

            # ── COPYRIGHT ASSESSMENT ───────────────────
            st.markdown("### ⚖️ Copyright Assessment")

            if top_score >= 70:
                st.error(
                    f"⚠️ HIGH SIMILARITY DETECTED ({top_score}%)\n\n"
                    "This content shows significant similarity to an existing "
                    "document. Proper attribution or licensing may be required."
                )
            elif top_score >= 40:
                st.warning(
                    f"🔔 MODERATE SIMILARITY DETECTED ({top_score}%)\n\n"
                    "This content has some similarity to existing documents. "
                    "A review is recommended before publishing."
                )
            else:
                st.success(
                    f"✅ LOW SIMILARITY ({top_score}%)\n\n"
                    "This content appears to be original. "
                    "No significant copyright concerns detected."
                )


# ── FOOTER ────────────────────────────────────────────
st.divider()
st.markdown("""
    <div style="text-align:center; color:#aaaaaa; font-size:0.8rem;">
        Built with Python · scikit-learn · Streamlit &nbsp;|&nbsp;
        For academic and IP monitoring research purposes
    </div>
""", unsafe_allow_html=True)