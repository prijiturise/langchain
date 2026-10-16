
import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# --------------------------------
# 1. Streamlit page configuration
# --------------------------------
st.set_page_config(
    page_title="Healthy Breakfast Ideas",
    page_icon="🌿",
    layout="centered",
)

# --------------------------------
# 2. Green agriculture theme
# --------------------------------
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
    '<p class="intro">Simple, nutritious breakfast ideas '
    'for a fresh start to your day.</p>',
    unsafe_allow_html=True,
)

st.divider()

st.subheader("🥗 Discover your next breakfast")
st.write(
    "Generate five practical breakfast ideas using "
    "nutritious ingredients and balanced portions."
)

# --------------------------------
# 3. Check API key
# --------------------------------
if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is not set. Please configure it "
        "in your terminal and restart Streamlit."
    )
    st.stop()

# --------------------------------
# 4. Create the language model
# --------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# --------------------------------
# 5. Create the prompt template
# --------------------------------
prompt = ChatPromptTemplate.from_template(
    """
    You are a nutrition-aware breakfast assistant.

    Suggest exactly 5 healthy breakfast ideas.

    Healthy means:
    - Include fiber-rich foods such as whole grains,
      fruits, vegetables, or legumes.
    - Include a useful source of protein where practical.
    - Prefer minimally processed ingredients.
    - Use reasonable portions and limit excess added sugar
      and oil.
    - Suggest practical, affordable home-cooked meals.

    Cuisine preference: {cuisine}

    Output rules:
    - Provide exactly 5 ideas.
    - Number them from 1 to 5.
    - Write one idea per line.
    - Name a specific breakfast dish.
    - Do not include an introduction, conclusion,
      explanations, or extra commentary.
    """
)

# --------------------------------
# 6. Create the output parser
# --------------------------------
parser = StrOutputParser()

# --------------------------------
# 7. Build the LangChain chain
# --------------------------------
chain = prompt | llm | parser

# --------------------------------
# 8. Streamlit user interaction
# --------------------------------
cuisine = st.selectbox(
    "Choose your breakfast preference",
    [
        "South Indian vegetarian",
        "Indian vegetarian",
        "Healthy international options",
    ],
)

if st.button("🌱 Generate 5 Breakfast Ideas", use_container_width=True):
    with st.spinner("Preparing your breakfast ideas..."):
        try:
            # Invoke the complete chain.
            result = chain.invoke({"cuisine": cuisine})

            st.subheader("Your 5 Healthy Breakfast Ideas")
            st.markdown(result)

        except Exception as e:
            st.error(f"Unable to generate ideas: {e}")

st.divider()
st.caption("🌱 Eat well. Live well. Start fresh.")
