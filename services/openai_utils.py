import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAI():

    def __init__(self):
        self.client = openai.OpenAI()

    def get_embedding(self, text, model="text-embedding-3-small"):
        response = openai.embeddings.create(
            input=[text],
            model=model,
        )
        return response.data[0].embedding



    def get_completion(self, prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=200):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content




