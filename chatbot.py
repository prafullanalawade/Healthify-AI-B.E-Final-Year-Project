import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the Flan-T5 model
model_name = "google/flan-t5-small"  # Or use other sizes like 'base' or 'large'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Generate a response with repetition penalty
def generate_answer(user_query):
    # Tokenize input
    inputs = tokenizer(user_query, return_tensors="pt")

    # Generate response with custom decoding parameters
    outputs = model.generate(
        inputs.input_ids,
        max_length=550,  # Increase the maximum length of the response
        min_length=50,   # Ensure the response is at least 50 tokens long
        temperature=0.7, # Adjust temperature for more diverse answers
        repetition_penalty=1.5,  # Penalize repeated phrases
        top_k=50,        # Limit to top 50 tokens for diversity
        top_p=0.9,       # Use nucleus sampling for better quality
        num_return_sequences=1,  # Generate only one response
        do_sample=True    # Enable sampling to encourage variety
    )

    # Decode response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit UI
def chatbot():
    st.title("Healthify-AI Chatbot")
    st.text("Ask any health-related question!")

    # User input
    user_query = st.text_input("Your Question:")

    if st.button("Get Answer"):
        if user_query:
            response = generate_answer(user_query)  # Call the updated function
            st.success(response)
        else:
            st.error("Please enter a question.")

if __name__ == "__main__":
    chatbot()
