
from src.keys import getHeaders
from langchain_huggingface import HuggingFacePipeline

from pydantic import BaseModel
from .schemas import Exercise


###
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

import json
###

def huggingface_example():
    import requests

    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = getHeaders()

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": "Who is the smartest person in the world?",
    })
    print(output)
from langchain_community.llms import Ollama

def ollama_phi3():
    """
    Description:
        - Creates phi3 ollama model
        - Parameters:
            - model = 'phi3'
            - temperature = 0.0
    Setup: 
        - (If not already done) Ollama pull phi3
    Return:
        - Returns the model
    """
    llm = Ollama(model='phi3', temperature=0.0) # temp defaults to 0.8

    return llm

import time
def prompt_model(query):

    model = ollama_phi3()

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Exercise)

    prompt = PromptTemplate(
        template="Return the name of the exercise, number of reps, number of sets, and the weight on the format specified.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    result = chain.invoke({"query": query})
    
    """
    ## Time info ollama:
    Initialising model time: 0.011039018630981445
    Chain assembly 0.01017308235168457
    Prompt time: 11.883311748504639
    Total: 11.904523849487305
    """

    return result


def goggins(query):

    model = ollama_phi3()

    prompt = PromptTemplate(
        template = "Reply as if you are David Goggins with excitement and profanity. Please include talking about the inner bitch or being a bitch, etc. when appropriate", 
        input_variables = ["query"]
    )

    chain = prompt | model

    result = chain.invoke({"query": query})

    return result


if __name__ == "__main__":

    #test_query = "Bench press for 3 sets, 8 reps each time with 60kg"
    test_query = "Squats 10 reps for 3 sets with 100kg "

    result = prompt_model(test_query)

    print(result)
