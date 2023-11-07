import google.generativeai as palm
import os

palm.configure(api_key=os.environ['BARD_API_KEY'])

def bard_trans(text):
  prompt = f"{text}"
  # print(prompt)

  defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.0,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  }
  response = palm.generate_text(
    **defaults,
    prompt=prompt
  )

  # response = palm.chat(messages=[f"""{text}"""])
  # print(response.result) #  'cold.'
  # return response.last

  return response.result