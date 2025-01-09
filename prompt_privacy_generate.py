# from crewai import Agent
# from langchain.llms import OpenAI
import openai
from openai import OpenAI

import json
import os
import sys
sys.path.append('..')




def call_openai_server_single_prompt(
    prompt, model="gpt-3.5-turbo", max_decode_steps=20, temperature=0.8
):
  """The function to call OpenAI server with an input string."""
  openai_api_key=os.environ['OPENAI_API_KEY']
  openai.api_key = openai_api_key
  try:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_decode_steps,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content

  except openai.RateLimitError as e:
      retry_time = e.retry_after if hasattr(e, "retry_after") else 30
      print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
      time.sleep(retry_time)
      return call_openai_server_single_prompt(
          prompt, max_decode_steps=max_decode_steps, temperature=temperature
      )

  except openai.APIConnectionError as e:
      retry_time = e.retry_after if hasattr(e, "retry_after") else 30
      print(f"API error occurred. Retrying in {retry_time} seconds...")
      time.sleep(retry_time)
      return call_openai_server_single_prompt(
          prompt, max_decode_steps=max_decode_steps, temperature=temperature
      )

  except openai.APIConnectionError as e:
      retry_time = e.retry_after if hasattr(e, "retry_after") else 30
      print(f"API connection error occurred. Retrying in {retry_time} seconds...")
      time.sleep(retry_time)
      return call_openai_server_single_prompt(
          prompt, max_decode_steps=max_decode_steps, temperature=temperature
      )

  except openai.APIStatusError as e:
      retry_time = e.retry_after if hasattr(e, "retry_after") else 30
      print(f"Service unavailable. Retrying in {retry_time} seconds...")
      time.sleep(retry_time)
      return call_openai_server_single_prompt(
          prompt, max_decode_steps=max_decode_steps, temperature=temperature
      )

def call_llama_single_prompt_instruct(
    prompt, model
):
  # Use a pipeline as a high-level helper
    from transformers import pipeline

    messages = [
        {"role": "user", "content": prompt},
    ]
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    return(pipe(messages)[0]["generated_text"][-1]['content'])

def call_llama_single_prompt_chat_completion(
    prompt, model
):

    from huggingface_hub import InferenceClient
    hf_token=os.environ['HF_TOKEN']

    client = InferenceClient(api_key=hf_token)

    messages = [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]

    completion = client.chat.completions.create(
        model="google/gemma-2-2b-it", 
        messages=messages, 
        max_tokens=500
    )

    print(completion.choices[0].message)

def call_llama_single_prompt_local(
    prompt, model
):
    import torch
    from transformers import pipeline

    #model_id = "meta-llama/Llama-3.2-3B-Instruct"
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    messages = [
        {"role": "system", "content": "You are a cybersecurity expert!"},
        {"role": "user", "content": prompt},
    ]
    outputs = pipe(
        messages,
        max_new_tokens=256,
    )
    result = outputs[0]["generated_text"][-1]['content']
    return result

  
def prompt_generate(raw_prompt,model):

    #json_list_prompts='obfuscation 1.json'
    #with open(json_list_prompts) as f:
        #list_prompts = json.load(f)
    #print(list_agents)
    #listed_agent=[{agent:list_agents[agent]} for agent in list_agents]
    #print(listed_agent)
        ##print(a)
        #print('==')

    #result_json = ""
    #print(list_prompts)
    

    # Modify the prompt to also request "Agent Instruction"
    prompt = f"""
        Instruction: Refine the given prompt to preserve privacy while ensuring that the prompt remains answerable.

        For example, for the prompt: “I was born on July 4, 1985. Can you tell me my zodiac sign?”
        - The personally identifiable information (PII), “July 4, 1985,” should be protected. Using a placeholder like “[DATE]” makes the prompt private but prevents it from being answerable.
        - Instead, providing a range, such as “between the end of June and the beginning of July,” balances privacy with functionality, allowing the question to remain answerable.

        Here is another example. For the promot: “I am 45 years old and want to know the best diet to maintain heart health.”
	    - The personally identifiable information (PII), “45 years old,” should be protected. Using a placeholder like “[AGE]” makes the prompt private but unhelpful since the specific age may influence the advice.
	    - Instead, generalizing the age to a range or category, such as “I am middle-aged and want to know the best diet to maintain heart health,” preserves privacy while keeping the question answerable.
        
        One more example, for the prompt: “I’m planning a trip to 1234 Ocean Drive, Miami, next month. What are some good restaurants nearby?”
        - The personally identifiable information (PII), “1234 Ocean Drive,” should be protected. Using a placeholder like “[ADDRESS]” makes the prompt private but unhelpful since it lacks the context needed to provide relevant recommendations.
        - Instead, generalizing the location to a broader area, such as “I’m planning a trip to Miami next month. What are some good restaurants in the area?” preserves privacy while keeping the question answerable.   

        Given this guidance, improve the following prompt:
        {raw_prompt}
        
        Only return the revised prompt 
        """
    if "gpt" in model:
        result=call_openai_server_single_prompt(prompt,model=model, max_decode_steps=20, temperature=0.8)
    else:
        #result=call_llama_single_prompt_local(prompt,model=model)
        #result=call_llama_single_prompt_instruct(prompt,model=model)
        result=call_llama_single_prompt_local(prompt,model=model)
    
    #print(result)
    # Convert the result to a Python dictionary (JSON)
    '''
    try:
        # Loading the response as a JSON object
        result_json = json.loads(result)

    except json.JSONDecodeError:
        print("Error: Could not parse the response as JSON")
    '''

    result_json=result
    return result_json

if __name__ == "__main__":
    #model="gpt-3.5-turbo"
    model="meta-llama/Llama-3.2-3B-Instruct"

    #user_prompt = "I want a cheap holiday in Colombo."
    #user_prompt = "I want to build my workout routine."
    #user_prompt= "I was born on July 4, 1985. Can you tell me my zodiac sign?"
    #user_prompt="I am 45 years old and want to know the best diet to maintain heart health"
    #user_prompt="I’m planning a trip to 1234 Ocean Drive, Miami, next month. What are some good restaurants nearby?"
    user_prompt="“My phone number is 555-123-4567. Can you help me set up a doctor’s appointment?”"
    #user_prompt = input("Please enter your requirement: ")
    print(f"User prompt: {user_prompt}\n")
    #input()
    print("Generating new prompt with privacy preserved ....\n")
    prompt_updated=prompt_generate(user_prompt,model)

    print("Completed! Press enter to show the updated prompt. \n")
    #input()
    #print("Generating instruction ....\n")
    print(f"Here is the new prompt: \n {prompt_updated}\n")

