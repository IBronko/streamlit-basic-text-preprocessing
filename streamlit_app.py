import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import json
from streamlit_lottie import st_lottie

# Adding the current project directory to NLTK data path
import nltk
nltk.data.path.append('/Users/UEAY/Documents/Projects/learning_nlp')

#st.write("Session states before run:", st.session_state)

#####################################
# Hide Streamlit branding
#####################################

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#####################################
# Display lottie file 
#####################################

col1, col2 = st.columns(2)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
lottie_coding = load_lottiefile("lottie.json")

with col1:
    st.title("Basic Text Preprocessing")

with col2:
    st_lottie(
    lottie_coding,
    speed=0.5,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    height=200,
    width=200,
    key=None,
    )

#####################################
# Initialize default session states
#####################################

if "re_text_case" not in st.session_state:
    st.session_state.re_text_case = ""
    
if "tokenized" not in st.session_state:
    st.session_state.tokenized = list()

if "normalized" not in st.session_state:
    st.session_state.normalized = list()
  
button_status_list = ["re_button_state", "to_button_state", "no_button_state"]

for status in button_status_list:
    if status not in st.session_state:
        st.session_state[status] = False

#####################################
# Noise removal with Regex
#####################################

st.subheader("Noise Removal with Regular Expression")

raw_text = st.text_area("Enter raw text here:", value="<h1> 123If you’re unsure of which datasets/models you’ll need, you can install the “popular” subset of NLTK data, on the command line type python -m nltk.downloader popular, or in the Python interpreter import nltk; nltk.download('popular')@!   </h1>")
re_pattern = st.text_area("Enter regular expression here:", value="\d|@|!|<.?h1>|\.")

choose_regex_method = st.radio("Select from the following pattern methods", ("Remove", "Find All"), help="Either remove or find the regex pattern in your raw text")
choose_case_method = st.radio("Additional options", ("None", "Lowercase", "Uppercase"))

def change_status_re():
   st.session_state.re_button_state = True 

regex_button = st.button("Show result", on_click=change_status_re)

if regex_button or st.session_state.re_button_state:
    # Either remove or find according to regex pattern
    if choose_regex_method == "Remove":
        re_text = re.sub(re_pattern, " ", raw_text)
    elif choose_regex_method == "Find All":
        re_text = "".join(re.findall(re_pattern, raw_text))
    # Option to lowercase or uppercase the result    
    if choose_case_method == "Lowercase":
        st.session_state["re_text_case"] = re_text.lower()
    elif choose_case_method == "Uppercase":
        st.session_state["re_text_case"] = re_text.upper()
    else:
        st.session_state["re_text_case"] = re_text
    
    st.subheader("Result:")
    st.write(st.session_state.re_text_case)

#####################################
# Tokenization
#####################################

if st.session_state.re_button_state:
    st.subheader("Tokenization with NLTK")
    
    def change_status_to():
        st.session_state.to_button_state = True 
    
    remove_duplicates = st.checkbox('Remove duplicates') 
    token_button = st.button("Tokenize result", on_click=change_status_to)
    
    if token_button or st.session_state.to_button_state:
        st.session_state.tokenized = word_tokenize(st.session_state.re_text_case) 
        if remove_duplicates:
            st.session_state.tokenized = list(set(st.session_state.tokenized))
        st.write(st.session_state.tokenized)
       
#####################################
# Text Normalization
#####################################

if st.session_state.re_button_state and st.session_state.to_button_state:
    st.subheader("Text Normalization with NLTK")
    st.text("Stemming and Lemmatization")
    
    def change_status_no():
        st.session_state.no_button_state = True
    
    remove_stopwords = st.checkbox('Remove english stopwords (lowercase for better results)')
    normalize_button = st.button("Normalize tokens", on_click=change_status_no)
    
    stopwords = set(stopwords.words("english"))
    
    if normalize_button or st.session_state.no_button_state:
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        st.session_state.normalized = [stemmer.stem(token) for token in st.session_state.tokenized]
        st.session_state.normalized = [lemmatizer.lemmatize(token) for token in st.session_state.tokenized]
        if remove_stopwords:
            st.session_state.normalized = [token for token in st.session_state.normalized if token not in stopwords]
        
        st.write(st.session_state.normalized)
        
        
#st.write("Session states after run:", st.session_state)
