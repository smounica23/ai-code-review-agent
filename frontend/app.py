import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "https://ai-code-review-agent-production-cee9.up.railway.app/api/v1")

st.set_page_config(page_title="AI Code Review Agent", layout="wide")
st.title("🔍 AI Code Review Agent")

tab1, tab2 = st.tabs(["📋 Paste Code", "📁 Upload File"])

code = ""
language = None
jira_ticket_id = ""

with tab1:
    code = st.text_area("Paste your code here", height=300, placeholder="def example():\n    pass")
    language = st.selectbox("Language", ["python", "javascript", "java"])
    jira_ticket_id = st.text_input(
        "Jira Ticket ID (optional)",
        placeholder="e.g. KAN-4",
        help="Enter a Jira ticket ID to check if code matches requirements"
    )

with tab2:
    uploaded = st.file_uploader("Upload source file", type=["py", "js", "java"])
    if uploaded:
        code = uploaded.read().decode("utf-8")
        ext = uploaded.name.split(".")[-1]
        language = {"py": "python", "js": "javascript", "java": "java"}.get(ext, "python")
        st.code(code, language=language)

if st.button("▶ Run Review", type="primary"):
    if not code:
        st.error("Please paste or upload code first")
    else:
        with st.spinner("Running AI code review..."):
            resp = requests.post(f"{API_URL}/review", json={
                "code": code,
                "language": language,
                "jira_ticket_id": jira_ticket_id if jira_ticket_id else None
            })
            if resp.status_code == 200:
                st.session_state["review"] = resp.json()
                st.session_state["history"] = []
                st.session_state["code"] = code
                st.rerun()
            else:
                st.error(f"Error: {resp.text}")

if "review" in st.session_state:
    r = st.session_state["review"]
    stored_code = st.session_state.get("code", "")

    # metrics row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Overall Score", f"{r['overall_score']:.1f}/10")
    c2.metric("🔴 Critical", r["critical_count"])
    c3.metric("🟠 High", r["high_count"])
    c4.metric("🟡 Medium", r["medium_count"])
    c5.metric("🟢 Low", r["low_count"])

    # summary
    with st.expander("📝 Review Summary", expanded=True):
        st.markdown(r["summary"])

    # issues
    st.subheader("Issues Found")
    severity_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    sorted_issues = sorted(r["issues"], key=lambda x: severity_order.index(x.get("severity", "LOW")))

    for issue in sorted_issues:
        icon = severity_icon.get(issue.get("severity"), "⚪")
        with st.expander(f"{icon} [{issue.get('severity')}] {issue.get('description', '')[:80]}"):
            st.caption(f"Category: {issue.get('category')}")
            st.caption(f"Lines: {issue.get('line_start')} - {issue.get('line_end')}")
            st.caption(f"Rule: {issue.get('rule_id', 'N/A')}")
            st.caption(f"Source: {issue.get('source')}")
            if issue.get("fix_suggestion"):
                st.code(issue["fix_suggestion"], language=r.get("language", "python"))

    # jira alignment section
    if r.get("alignment_score") is not None and r.get("alignment_issues"):
        st.divider()
        st.subheader("📋 Jira Requirement Alignment")
        st.metric("Alignment Score", f"{r['alignment_score']:.1f}/10")
        if r["alignment_issues"]:
            st.warning("**Missing or incomplete requirements:**")
            for issue in r["alignment_issues"]:
                st.write(f"• {issue}")
    if r.get("code_suggestions"):
        st.divider()
        st.subheader("💡 Suggested Implementations")
        for suggestion in r.get("code_suggestions", []):
            with st.expander(f"📝 {suggestion.get('requirement', '')[:80]}"):
                st.caption(suggestion.get("explanation", ""))
                if suggestion.get("suggested_code"):
                    st.code(suggestion["suggested_code"], language=r.get("language", "python"))
                if suggestion.get("imports_needed"):
                    st.caption("Imports needed: " + ", ".join(suggestion.get("imports_needed", [])))

    # follow-up Q&A
    st.divider()
    st.subheader("💬 Ask a Follow-up Question")
    if "history" not in st.session_state:
        st.session_state["history"] = []

    for msg in st.session_state["history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if question := st.chat_input("Ask about any finding..."):
        st.session_state["history"].append({"role": "user", "content": question})
        resp = requests.post(f"{API_URL}/followup", json={
            "review_id": r["review_id"],
            "question": question,
            "conversation_history": st.session_state["history"],
            "code": stored_code,
            "issues": r["issues"]
        })
        answer = resp.json().get("answer", "Sorry, could not process that.")
        st.session_state["history"].append({"role": "assistant", "content": answer})
        st.rerun()