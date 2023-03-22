import streamlit as st
import openai

# Set up OpenAI API client
openai.api_key = st.secrets["API_KEY"]


# function to get list of tasks
def generate_cyu():
    st.session_state.flow = 1

    # Generate diverse persona

    cyu = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"""The content of an education lesson is as follows: {st.session_state.content}
            
            Create {st.session_state.question_num} multiple-choice questions with at least four possible responses
            for each question related to this content. 
                              
            These questions should reflect higher levels of Bloom's taxonomy when possible.
            
            Output the question, four answer choices, the correct answer, and level of Bloom's taxonomy as 
            separate columns in a table."""}
        ],
        temperature=0.6
    )

    st.session_state.cyu = cyu.choices[0]['message']['content']


def return_to_generator():
    st.session_state.flow = 0


if 'flow' not in st.session_state or st.session_state.flow == 0:
    st.session_state.flow = 0

    st.title("Check Your Understanding Question Generator :pencil:")

    st.markdown("### Greetings, let's create some check your understanding questions!")

    # Get user input
    st.session_state.question_num = st.number_input("How many questions to generate?", min_value=1, max_value=10)

    st.session_state.content = st.text_input("Paste in a transcript, description of the lesson content,"
                                             " or topic  (500 word limit):")

    st.button("Get me some questions!", on_click=generate_cyu, args="")

if st.session_state.flow == 1:
    st.write("Here are your questions:")
    st.markdown(st.session_state.cyu)
    st.text("-----------------")


    st.text("")
    st.text("")

    st.button("Roll the dice! (Give me more questions.) ", on_click=generate_cyu, args="")
    st.button("Go back to CYU generator.", on_click=return_to_generator, args="")
