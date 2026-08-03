"""
Streamlit chat interface for the Music Recommender ("MoodMatch chat").

Type a request in plain English -- "chill lofi for studying, acoustic" -- and
the app recommends songs; ask a question -- "what is lofi?" -- and it answers
from the knowledge base. Routing between those two behaviors is handled by the
agentic workflow in src/agent.py (plan -> act -> check -> respond), and every
message shows both what preferences were parsed and the agent's reasoning steps.

Run it from the project root:

    streamlit run src/chat_app.py

Everything runs fully offline with no API key. An OPTIONAL Gemini layer
(mirroring the class RAG notebook's ask_gemini) can rephrase a recommendation
into a conversational reply when a GEMINI_API_KEY is set and `google-genai` is
installed; it never chooses songs, so it cannot hallucinate recommendations.
"""

import os

import streamlit as st

# Support both `streamlit run src/chat_app.py` and package-style imports.
try:
    from src.agent import Agent, format_trace
except ModuleNotFoundError:
    from agent import Agent, format_trace


# --- Cached resources ------------------------------------------------------
@st.cache_resource
def get_agent():
    """Build the agent (loads catalog + knowledge docs + vocab) once."""
    return Agent()


# --- Optional Gemini rephrasing layer --------------------------------------
def _gemini_client():
    """
    Return a Gemini client if a key is set AND `google-genai` is installed,
    else None. All failures are swallowed so the chat never depends on it.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        return None
    try:
        from google import genai  # optional dependency, imported lazily
    except ImportError:
        return None
    try:
        return genai.Client()
    except Exception:
        return None


def rephrase_with_gemini(client, user_text: str, deterministic_reply: str) -> str:
    """
    Rephrase the already-chosen picks conversationally, grounded ONLY in them.
    Any failure falls back to the deterministic reply (fail closed).
    """
    prompt = (
        "Rephrase the recommendation list below into a warm, conversational reply "
        "(2-4 sentences plus the songs). Use ONLY the songs and facts given -- do "
        "not invent songs, artists, genres, or details, and keep every song's "
        "honest caveats.\n\n"
        f"<recommendations>\n{deterministic_reply}\n</recommendations>\n\n"
        f"The user asked: {user_text}"
    )
    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            generation_config={"thinking_level": "minimal"},
        )
        return interaction.output_text
    except Exception:
        return deterministic_reply


# --- App -------------------------------------------------------------------
def _render_transparency(prefs, trace_text):
    """Show the parsed preferences and the agent's reasoning trace."""
    with st.expander("What I understood"):
        st.write(prefs or "no taste preferences detected")
    with st.expander("Agent steps"):
        st.code(trace_text or "(no steps)", language="text")


def main() -> None:
    st.set_page_config(page_title="MoodMatch Chat", page_icon="🎧")
    st.title("🎧 MoodMatch — Music Recommender Chat")
    st.caption(
        "Ask for music (\"chill lofi for studying\") or ask a question "
        "(\"what is lofi?\"). I route each message to the right tool."
    )

    agent = get_agent()
    client = _gemini_client()

    # Sidebar: controls + catalog panel.
    with st.sidebar:
        st.header("Options")
        conversational = st.toggle(
            "Conversational replies (Gemini)",
            value=False,
            disabled=client is None,
            help=(
                "Rephrases recommendations into a chattier reply. Requires "
                "GEMINI_API_KEY and the google-genai package."
                if client is None else
                "Rephrases recommendations; the songs are still chosen offline."
            ),
        )
        if client is None:
            st.caption("Offline mode — set GEMINI_API_KEY and install google-genai to enable.")
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.subheader(f"Catalog ({len(agent.songs)} songs)")
        genres = sorted({s["genre"] for s in agent.songs})
        moods = sorted({s["mood"] for s in agent.songs})
        st.caption("**Genres:** " + ", ".join(genres))
        st.caption("**Moods:** " + ", ".join(moods))
        st.caption("Ask _\"what is <genre>?\"_ to learn about any of them.")

    # History (re-render prior turns, including their transparency panels).
    st.session_state.setdefault("messages", [])
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                _render_transparency(message.get("prefs"), message.get("trace"))

    # New turn.
    if user_text := st.chat_input("Ask for music, or ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        result = agent.run(user_text)
        reply = result.reply
        # Only rephrase real recommendations, never a doc answer or a hint.
        if conversational and client is not None and result.intent == "recommend":
            reply = rephrase_with_gemini(client, user_text, reply)

        trace_text = format_trace(result)
        st.session_state.messages.append({
            "role": "assistant", "content": reply,
            "prefs": result.prefs, "trace": trace_text,
        })
        with st.chat_message("assistant"):
            st.markdown(reply)
            _render_transparency(result.prefs, trace_text)


if __name__ == "__main__":
    main()
else:
    # Streamlit executes this module top-to-bottom rather than via __main__.
    main()
