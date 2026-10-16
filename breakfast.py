
import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ==========================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Healthy Breakfast Ideas",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# 2. GREEN AGRICULTURE THEME
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f3f8ef;
    }

    h1, h2, h3 {
        color: #245c35;
    }

    .intro {
        color: #42664a;
        font-size: 17px;
    }

    .stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #1b5e20;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌿 Healthy Breakfast Ideas")

st.markdown(
    '<p class="intro">Fresh, nutritious breakfast inspiration '
    'for a healthier start to your day.</p>',
    unsafe_allow_html=True,
)

st.divider()

st.subheader("🥗 Discover your next breakfast")

st.write(
    "Choose your preferred cuisine and generate five "
    "healthy breakfast ideas. Each new request will try "
    "to avoid previously suggested dishes."
)

# ==========================================
# 3. SESSION STATE
# Remember previously generated ideas
# ==========================================
if "previous_ideas" not in st.session_state:
    st.session_state.previous_ideas = []

if "current_ideas" not in st.session_state:
    st.session_state.current_ideas = ""

# ==========================================
# 4. CHECK OPENAI API KEY
# ==========================================
if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is missing. Set your API key "
        "in PowerShell and restart the application."
    )
    st.stop()

# ==========================================
# 5. CREATE CHAT MODEL
# ==========================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9,
)

# ==========================================
# 6. CREATE PROMPT TEMPLATE
# ==========================================
prompt = ChatPromptTemplate.from_template(
    """
    You are a creative, nutrition-aware breakfast assistant.

    Generate exactly 5 healthy breakfast ideas.

    Cuisine preference: {cuisine}

    Previously suggested breakfast ideas:
    {previous_ideas}

    What makes a breakfast healthy:
    - Include fiber-rich foods such as whole grains,
      vegetables, fruits, or legumes.
    - Include useful sources of protein where practical.
    - Prefer minimally processed ingredients.
    - Use reasonable portions and limit excess added sugar
      and oil.
    - Suggest affordable, practical home-cooked meals.

    Variety requirements:
    - Do not repeat any previously suggested dish.
    - Avoid minor variations of an existing dish.
    - Explore different ingredients and cooking methods.
    - Make all five ideas distinct from each other.
    - If the cuisine is South Indian vegetarian, prioritize
      suitable dishes from that cuisine.

    Output requirements:
    - Exactly 5 ideas.
    - Number them from 1 to 5.
    - Write exactly one line per idea.
    - Give a specific dish name.
    - No introduction, conclusion, or extra commentary.
    """
)

# ==========================================
# 7. CREATE OUTPUT PARSER
# ==========================================
parser = StrOutputParser()

# ==========================================
# 8. BUILD LANGCHAIN CHAIN
# ==========================================
chain = prompt | llm | parser

# ==========================================
# 9. CUISINE SELECTION
# ==========================================
cuisine = st.selectbox(
    "🍽️ Choose your breakfast preference",
    [
        "South Indian vegetarian",
        "Indian vegetarian",
        "Healthy international options",
    ],
)

# ==========================================
# 10. GENERATE NEW BREAKFAST IDEAS
# ==========================================
if st.button(
    "🌱 Generate 5 New Breakfast Ideas",
    use_container_width=True,
):
    with st.spinner("Preparing fresh breakfast ideas..."):
        try:
            # Supply the history to the prompt
            previous_ideas = "\n".join(
                st.session_state.previous_ideas
            )

            # Invoke the complete LangChain chain
            result = chain.invoke(
                {
                    "cuisine": cuisine,
                    "previous_ideas": (
                        previous_ideas
                        if previous_ideas
                        else "None yet"
                    ),
                }
            )

            # Store the latest result
            st.session_state.current_ideas = result

            # Save the individual numbered lines
            ideas = [
                line.strip()
                for line in result.splitlines()
                if line.strip()
            ]

            for idea in ideas:
                if idea not in st.session_state.previous_ideas:
                    st.session_state.previous_ideas.append(idea)

        except Exception as e:
            st.error(f"Unable to generate ideas: {e}")

# ==========================================
# 11. DISPLAY RESULTS
# ==========================================
if st.session_state.current_ideas:
    st.divider()
    st.subheader("🥣 Your Healthy Breakfast Ideas")
    st.markdown(st.session_state.current_ideas)

# ==========================================
# 12. RESET HISTORY
# ==========================================
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.caption(
        f"🌱 Previous suggestions remembered: "
        f"{len(st.session_state.previous_ideas)}"
    )

with col2:
    if st.button("🔄 Reset History"):
        st.session_state.previous_ideas = []
        st.session_state.current_ideas = ""
        st.rerun()

st.caption("🌿 Eat well. Live well. Start fresh.")
