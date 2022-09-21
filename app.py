import streamlit as st
import joblib
from youtube_comments import extract_comments
import string
from nltk.corpus import stopwords
import pandas as pd


def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    STOPWORDS = stopwords.words('english') + ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])

@st.cache(allow_output_mutation=True)
def load_model():
    model = joblib.load('model.joblib')
    return model

# Loading the model from file
model = load_model()

# Function to predict spam and ham, given a text
def predict(txt):
    prediction = model.predict([txt])
    if prediction[0] == 1:
        return "Spam"
    else:
        return "Not Spam"

# USER INTERFACE
# Creating the heading
st.title('Spam Detection App')

# Retrieving and storing the text from the textbox
txt = st.text_area('Text to analyze', )

# predicting the class and writing it on the webpage
st.write('Predictions:', predict(txt))

# Getting the YouTube URL
youtube_url = st.text_input('YouTube URL', )

# Getting the custom messages dataset
uploaded_file = st.file_uploader("Choose a file")

# If a custom dataset is uploaded, then create a histogram for that else if
# YouTube URL is provided, extract the comments from there and create the histogram of prediction

if st.button('Compute'):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='latin-1')
        result_data = [0, 0]
        for each in df['Text']:
            pred_data = predict(text_process(each))
            if pred_data == 'Spam':
                result_data[0] += 1
            else:
                result_data[1] += 1
        result = pd.DataFrame({'Spam':[result_data[0]], 'Not Spam':[result_data[1]]}, columns=['Spam', 'Not Spam'])
        st.bar_chart(data=result)
    else:
        comments = extract_comments(youtube_url)
        processed_data = []
        final_count = [0, 0]
        for key, val in comments.items():
            pred_data = predict(text_process(val[0]))
            if pred_data == 'Spam':
                processed_data.append(1)
                final_count[0] += 1
            else:
                processed_data.append(0)
                final_count[1] += 1

        chart_data = pd.DataFrame({'Spam': [final_count[0]], 'Not Spam': [final_count[1]]}, columns=['Spam', 'Not Spam'])
        st.bar_chart(chart_data)

else:
    pass

