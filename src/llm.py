
from src.keys import getHeaders
from langchain_huggingface import HuggingFacePipeline

from pydantic import BaseModel


###
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

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

def ollama_phi3(query):
    """
    Description:
        - Prompts phi3 (temperature=0.0)
    Setup: 
        - (If not already done) Ollama pull phi3
    Return:
        - Returns the LLM response
    """
    llm = Ollama(model='phi3', temperature=0.0) # temp defaults to 0.8
    result = llm.invoke(query)

    return result   

if __name__ == "__main__":

     
    model = Ollama(model='phi3', temperature=0.0)


    class Pipeline(BaseModel):
        parameter: str = Field(description="Name of analytes, e.g. HBA1", max_length=20)
        value: str = Field(description="Value of analytes, e.g. 10.2", max_length=10)
        unit: str = Field(description="Unit of the value is measured in, e.g. mmol/L", max_length=10)


    # And a query intented to prompt a language model to populate the data structure.
    query = f"""
            From each of the following dictionaries value extract the paramater, value, and unit of the analyte.
            Dictionaries: [{{"Total Testosterone": "Total Testosterone (Siemens) 39.2 nmol/L (8.3-29)"}}, {{"Iron": "Iron (10-30) umol/L 40 33 21 27"}}]
    """

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Pipeline)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    result = chain.invoke({"query": query})

    print(f"All: {result}\n")

    print(f"Result one: {result[0]}")
    print(f"Result one, parameter: {result[0]['parameter']}")
    print(f"Result one, value: {result[0]['value']}")
    print(f"Result one, unit: {result[0]['unit']}\n")

    print(f"Result two: {result[1]}")
    print(f"Result two, parameter: {result[1]['parameter']}")
    print(f"Result two, value: {result[1]['value']}")