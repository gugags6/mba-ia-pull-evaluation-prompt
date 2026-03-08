"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Fluxo:
1. Lê prompts/bug_to_user_story_v2.yml
2. Valida estrutura
3. Reconstrói ChatPromptTemplate
4. Faz push PÚBLICO para o LangSmith Hub
5. Adiciona descrição e tags
"""

"""
Push de prompt customizado para LangSmith Hub
Converte YAML customizado para ChatPromptTemplate automaticamente.
"""

import os
import re
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_FILE_PATH = "../prompts/bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


# ==========================================================
# EXTRAIR VARIÁVEIS DO TEMPLATE
# ==========================================================

def extract_variables(text: str) -> list:
    """
    Extrai variáveis no formato:
    {var} ou {{var}}
    """
    matches = re.findall(r"\{\{?(\w+)\}?\}", text)
    return list(set(matches))


# ==========================================================
# CONVERTER YAML → ChatPromptTemplate
# ==========================================================

def build_chat_prompt(prompt_data: dict) -> ChatPromptTemplate:
    """
    Converte seu formato YAML customizado
    para ChatPromptTemplate válido.
    """

    system_prompt = prompt_data.get("system")
    user_prompt = prompt_data.get("user")

    if not system_prompt or not user_prompt:
        raise ValueError("Campos 'system' e 'user' são obrigatórios.")

    # Extrai variáveis automaticamente
    variables = extract_variables(system_prompt + user_prompt)

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    ).partial() if not variables else ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )


# ==========================================================
# PUSH
# ==========================================================

def push_prompt(username: str, prompt_data: dict):

    print_section_header("Construindo ChatPromptTemplate")

    prompt = build_chat_prompt(prompt_data)

    prompt_name = f"{username}/{PROMPT_KEY}"

    print(f"Fazendo push: {prompt_name}")

    hub.push(
        prompt_name,
        prompt
       
    )

    print("Push realizado com sucesso!")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print_section_header("INICIANDO PUSH")

    check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"])

    data = load_yaml(PROMPT_FILE_PATH)

    if PROMPT_KEY not in data:
        print(f"Chave '{PROMPT_KEY}' não encontrada no YAML.")
        return 1

    prompt_data = data[PROMPT_KEY]

    username = os.getenv("USERNAME_LANGSMITH_HUB")

    try:
        push_prompt(username, prompt_data)
        print_section_header("PUSH FINALIZADO COM SUCESSO")
        return 0
    except Exception as e:
        print("Erro ao fazer push:")
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())