"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = Path("prompts/bug_to_user_story_v1.yml")


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt do LangSmith Hub e salva localmente como YAML.
    """
    print_section_header("Conectando ao LangSmith Prompt Hub")

    # Valida variáveis obrigatórias
    check_env_vars(["LANGSMITH_API_KEY", "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"])

    try:
        print(f"Fazendo pull do prompt: {PROMPT_NAME}")
        prompt = hub.pull(PROMPT_NAME)

        # Serializa o prompt para dict
        prompt_dict = prompt.dict()

        print("Prompt puxado com sucesso!")
        return prompt_dict

    except Exception as e:
        print(f"Erro ao fazer pull do prompt: {e}")
        sys.exit(1)


def main():
    print_section_header("INICIANDO PULL DE PROMPTS")

    prompt_data = pull_prompts_from_langsmith()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(prompt_data, OUTPUT_PATH)

    print(f"Prompt salvo em: {OUTPUT_PATH}")
    print("Pull finalizado com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
