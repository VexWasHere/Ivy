from gpt4all import GPT4All
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM

while True:
    try:
        user_input = input("You: ")
        with model.chat_session():
            print(f"Ivy: {model.generate(user_input, max_tokens=1024)}")
    except Exception as e:
        print("Error: ", e)