import os

from openai import OpenAI


client = OpenAI()
completion = client.chat.completions.create(
  model="dall-e-3",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].json)

