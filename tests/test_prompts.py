"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# pyrefly: ignore [missing-import]
from utils import validate_prompt_structure

def load_prompt_data():
    file_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data.get('bug_to_user_story_v2', {})

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system' existe e não está vazio."""
        data = load_prompt_data()
        assert 'system' in data
        assert data['system'].strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        data = load_prompt_data()
        system_text = data.get('system', '').lower()
        assert 'você é' in system_text or 'voce e' in system_text or 'act as' in system_text or 'aja como' in system_text

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        data = load_prompt_data()
        system_text = data.get('system', '').lower()
        assert 'markdown' in system_text or 'user story' in system_text or 'como um' in system_text

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        data = load_prompt_data()
        system_text = data.get('system', '').lower()
        # Verificar se a palavra 'exemplo' ou similar existe no system prompt
        assert 'exemplo' in system_text or 'example' in system_text

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        data = load_prompt_data()
        system_text = data.get('system', '')
        assert '[TODO]' not in system_text and '[todo]' not in system_text.lower()

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        data = load_prompt_data()
        assert 'tags' in data
        assert len(data['tags']) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])