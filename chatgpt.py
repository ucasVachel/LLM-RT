import openai
import os

# This class instantiate the API, used to communicate with GPT
class ChatGPT:
    def __init__(self, method):
        self.id = 0
        
    def ask(self, prompt, stop=["\n"], max_tokens=100):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=max_tokens,
            stop=stop
        )
        return response.choices[0].message.content

    
    def chat(self, query, prompt="", stop=["\n"], max_tokens=100):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": query},
                {"role": "assistant", "content": prompt}
            ],
            temperature=0,
            max_tokens=max_tokens,
            stop=stop
        )
        return response["choices"][0]["message"]["content"]
    
    def chat_with_image(self, chat_history, stop=["\n"], max_tokens=100):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]