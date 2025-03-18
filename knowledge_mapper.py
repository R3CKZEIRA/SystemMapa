import json
import os
import sys
from datetime import datetime

class KnowledgeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def add_child(self, name):
        child = KnowledgeNode(name, self)
        self.children.append(child)
        return child
    
    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "children": [child.to_dict() for child in self.children]
        }
    
    @classmethod
    def from_dict(cls, data, parent=None):
        node = cls(data["name"], parent)
        node.id = data.get("id", node.id)
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data, node)
            node.children.append(child)
        return node

class KnowledgeMap:
    def __init__(self, name):
        self.root = KnowledgeNode(name)
        self.current_theme = name
    
    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"Mapa de conhecimento salvo em {filename}")
    
    def load(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.root = KnowledgeNode.from_dict(data)
            self.current_theme = self.root.name
            print(f"Mapa de conhecimento carregado de {filename}")
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado.")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo JSON {filename}.")
    
    def display(self, node=None, level=0):
        if node is None:
            node = self.root
        
        prefix = "  " * level
        print(f"{prefix}{'└─' if level > 0 else ''} {node.name}")
        
        for child in node.children:
            self.display(child, level + 1)
    
    def add_node(self, path, new_node_name):
        """Adiciona um novo nó no caminho especificado"""
        if not path:  # Adicionar ao nó raiz
            self.root.add_child(new_node_name)
            return True
        
        current = self.root
        for name in path:
            found = False
            for child in current.children:
                if child.name == name:
                    current = child
                    found = True
                    break
            if not found:
                print(f"Caminho não encontrado: {name}")
                return False
        
        current.add_child(new_node_name)
        return True
    
    def reverse_engineer(self, source_text, original_domain, target_domain):
        """Realiza engenharia reversa simples substituindo termos"""
        # Mapeamento de termos entre domínios
        if original_domain == "Gestão do Conhecimento" and target_domain == "TDAH":
            mapping = {
                "Gestão do Conhecimento": "TDAH",
                "Conhecimento Tácito": "Déficit de Atenção",
                "Conhecimento Explícito": "Hiperatividade",
                "Conversão de Conhecimento": "Impulsividade",
                "Criação": "Diagnóstico",
                "Armazenamento": "Avaliação",
                "Compartilhamento": "Tratamento",
                "Aplicação": "Gestão Diária"
            }
        elif original_domain == "TDAH" and target_domain == "Gestão do Conhecimento":
            mapping = {
                "TDAH": "Gestão do Conhecimento",
                "Déficit de Atenção": "Conhecimento Tácito",
                "Hiperatividade": "Conhecimento Explícito",
                "Impulsividade": "Conversão de Conhecimento",
                "Diagnóstico": "Criação",
                "Avaliação": "Armazenamento",
                "Tratamento": "Compartilhamento",
                "Gestão Diária": "Aplicação"
            }
        else:
            mapping = {}
        
        result = source_text
        for original, replacement in mapping.items():
            result = result.replace(original, replacement)
        
        return result
    
    def generate_prompt(self, prompt_type):
        """Gera um prompt baseado no tipo selecionado"""
        prompts = {
            "map": f"Mapeie os principais conceitos relacionados a {self.current_theme}, organizando-os em categorias e subcategorias.",
            "structure": f"Crie uma estrutura hierárquica para organizar o conhecimento sobre {self.current_theme}.",
            "reverse": f"Analise a seguinte estrutura de conhecimento e identifique os padrões utilizados para organizá-la.",
            "adapt": f"Adapte a estrutura de conhecimento para um novo domínio, mantendo a mesma organização hierárquica.",
            "validate": f"Avalie a estrutura de conhecimento e identifique possíveis lacunas ou inconsistências."
        }
        return prompts.get(prompt_type, "Prompt não encontrado.")

def create_example_knowledge_map(theme):
    """Cria um mapa de conhecimento de exemplo"""
    km = KnowledgeMap(theme)
    
    if theme == "Gestão do Conhecimento":
        # Criar estrutura para Gestão do Conhecimento
        conceitos = km.root.add_child("Conceitos Fundamentais")
        conceitos.add_child("Conhecimento Tácito")
        conceitos.add_child("Conhecimento Explícito")
        conceitos.add_child("Conversão de Conhecimento")
        
        processos = km.root.add_child("Processos")
        processos.add_child("Criação de Conhecimento")
        processos.add_child("Armazenamento")
        processos.add_child("Compartilhamento")
        processos.add_child("Aplicação")
        
        ferramentas = km.root.add_child("Ferramentas")
        ferramentas.add_child("Sistemas de GC")
        ferramentas.add_child("Comunidades de Prática")
        ferramentas.add_child("Taxonomias e Ontologias")
        
        metricas = km.root.add_child("Métricas e Avaliação")
        metricas.add_child("ROI do Conhecimento")
        metricas.add_child("Modelos de Maturidade")
    
    elif theme == "TDAH":
        # Criar estrutura para TDAH
        conceitos = km.root.add_child("Conceitos Fundamentais")
        conceitos.add_child("Déficit de Atenção")
        conceitos.add_child("Hiperatividade")
        conceitos.add_child("Impulsividade")
        
        diagnostico = km.root.add_child("Diagnóstico")
        diagnostico.add_child("Critérios Diagnósticos")
        diagnostico.add_child("Avaliação Clínica")
        diagnostico.add_child("Diagnóstico Diferencial")
        
        tratamento = km.root.add_child("Tratamento")
        tratamento.add_child("Medicação")
        tratamento.add_child("Terapia Comportamental")
        tratamento.add_child("Coaching para TDAH")
        
        gestao = km.root.add_child("Gestão Diária")
        gestao.add_child("Estratégias de Organização")
        gestao.add_child("Ferramentas de Apoio")
    
    return km

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """Menu principal do sistema"""
    km = None
    current_file = None
    
    while True:
        clear_screen()
        print("\n===== SISTEMA DE MAPEAMENTO DE CONHECIMENTOS =====")
        print("1. Criar novo mapa de conhecimento")
        print("2. Carregar mapa existente")
        print("3. Usar exemplo: Gestão do Conhecimento")
        print("4. Usar exemplo: TDAH")
        print("5. Sair")
        
        if km:
            print("\n----- OPERAÇÕES NO MAPA ATUAL -----")
            print("6. Visualizar mapa")
            print("7. Adicionar nó")
            print("8. Salvar mapa")
            print("9. Gerar prompt")
            print("10. Engenharia reversa")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            name = input("Nome do novo mapa de conhecimento: ")
            km = KnowledgeMap(name)
            print(f"Mapa '{name}' criado com sucesso!")
        
        elif choice == "2":
            filename = input("Nome do arquivo para carregar: ")
            km = KnowledgeMap("")
            km.load(filename)
            current_file = filename
        
        elif choice == "3":
            km = create_example_knowledge_map("Gestão do Conhecimento")
            print("Exemplo de Gestão do Conhecimento carregado!")
        
        elif choice == "4":
            km = create_example_knowledge_map("TDAH")
            print("Exemplo de TDAH carregado!")
        
        elif choice == "5":
            print("Saindo do sistema...")
            break
        
        elif choice == "6" and km:
            clear_screen()
            print(f"\nMapa de Conhecimento: {km.current_theme}\n")
            km.display()
            input("\nPressione Enter para continuar...")
        
        elif choice == "7" and km:
            path_str = input("Caminho para adicionar (separado por '>'): ")
            path = [p.strip() for p in path_str.split(">")] if path_str else []
            node_name = input("Nome do novo nó: ")
            if km.add_node(path, node_name):
                print(f"Nó '{node_name}' adicionado com sucesso!")
            input("Pressione Enter para continuar...")
        
        elif choice == "8" and km:
            filename = input("Nome do arquivo para salvar: ")
            km.save(filename)
            current_file = filename
            input("Pressione Enter para continuar...")
        
        elif choice == "9" and km:
            clear_screen()
            print("\n===== GERADOR DE PROMPTS =====")
            print("1. Mapeamento de Conceitos")
            print("2. Estruturação Hierárquica")
            print("3. Engenharia Reversa")
            print("4. Adaptação para Novo Domínio")
            print("5. Validação de Conhecimento")
            
            prompt_choice = input("\nEscolha um tipo de prompt: ")
            prompt_types = {
                "1": "map",
                "2": "structure",
                "3": "reverse",
                "4": "adapt",
                "5": "validate"
            }
            
            if prompt_choice in prompt_types:
                prompt = km.generate_prompt(prompt_types[prompt_choice])
                print("\nPrompt Gerado:")
                print("-" * 50)
                print(prompt)
                print("-" * 50)
            else:
                print("Opção inválida!")
            
            input("\nPressione Enter para continuar...")
        
        elif choice == "10" and km:
            clear_screen()
            print("\n===== ENGENHARIA REVERSA =====")
            source_text = input("Cole o texto fonte para análise: ")
            original_domain = input("Domínio original: ")
            target_domain = input("Domínio alvo: ")
            
            result = km.reverse_engineer(source_text, original_domain, target_domain)
            
            print("\nResultado da Engenharia Reversa:")
            print("-" * 50)
            print(result)
            print("-" * 50)
            
            input("\nPressione Enter para continuar...")
        
        else:
            if km is None and choice in ["6", "7", "8", "9", "10"]:
                print("Primeiro crie ou carregue um mapa de conhecimento!")
            else:
                print("Opção inválida!")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main_menu()

