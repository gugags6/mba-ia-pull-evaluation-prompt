import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from utils import get_llm
from metrics import evaluate_f1_score

load_dotenv()

def main():
    client = Client()
    prompt_name = "gugags6/bug_to_user_story_v2"
    prompt = hub.pull(prompt_name)
    llm = get_llm(temperature=0)
    chain = prompt | llm
    
    examples = list(client.list_examples(dataset_name="prompt-optimization-challenge-resolved-eval"))
    
    for i, example in enumerate(examples[:3]):
        print(f"\n--- EXEMPLO {i+1} ---")
        inputs = example.inputs
        outputs = example.outputs
        
        response = chain.invoke(inputs)
        answer = response.content
        reference = outputs.get("reference", "")
        
        print("GERADO:\n" + answer)
        print("\nESPERADO:\n" + reference)
        
        #f1 = evaluate_f1_score(inputs.get("bug_report", ""), answer, reference)
        #print(f"\nF1 SCORE: {f1['score']}")
        #print(f"REASONING: {f1['reasoning']}")

if __name__ == "__main__":
    main()
