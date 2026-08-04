import gradio as gr

def chatbot(message, history):
    return f"You asked: {message}"

demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 AI Expert for Kids",
    description="""
Ask any AI question.
The AI explains concepts for kids aged 5-15 years.
"""
)

demo.launch()
