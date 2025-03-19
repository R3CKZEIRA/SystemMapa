from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

# Garantir que a pasta de dados existe
os.makedirs('data', exist_ok=True)

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
        filepath = os.path.join('data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f, indent=2, ensure_ascii=False)
        return f"Mapa de conhecimento salvo em {filepath}"
    
    def load(self, filename):
        filepath = os.path.join('data', filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.root = KnowledgeNode.from_dict(data)
            self.current_theme = self.root.name
            return f"Mapa de conhecimento carregado de {filepath}"
        except FileNotFoundError:
            return f"Arquivo {filepath} não encontrado."
        except json.JSONDecodeError:
            return f"Erro ao decodificar o arquivo JSON {filepath}."
    
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

# Função para criar visualização do mapa de conhecimento (orientação horizontal)
def create_knowledge_map(structure, level=0, parent=None, G=None, pos=None, node_count=None):
    if G is None:
        G = nx.Graph()
        pos = {}
        node_count = {"total": 0, "level": {}}
    
    if level not in node_count["level"]:
        node_count["level"][level] = 0
    
    current_node = f"{level}_{node_count['level'][level]}"
    G.add_node(current_node, name=structure["name"], level=level)
    
    # Posicionamento dos nós em níveis (horizontal - da esquerda para direita)
    if level == 0:
        pos[current_node] = (0, 0)
    else:
        siblings = node_count["level"][level]
        # Invertemos x e y para orientação horizontal
        pos[current_node] = (level, siblings - (len(structure.get("children", [])) / 2))
    
    if parent is not None:
        G.add_edge(parent, current_node)
    
    node_count["level"][level] += 1
    node_count["total"] += 1
    
    for child in structure.get("children", []):
        create_knowledge_map(child, level+1, current_node, G, pos, node_count)
    
    return G, pos

# Função para renderizar o mapa de conhecimento como imagem (corrigida)
def render_knowledge_map_image(structure):
    G, pos = create_knowledge_map(structure)
    
    plt.figure(figsize=(14, 10))
    
    # Desenhar nós por nível com cores diferentes
    node_colors = []
    node_sizes = []
    labels = {}
    
    for node in G.nodes():
        level = G.nodes[node]["level"]
        if level == 0:
            node_colors.append("#7c3aed")  # Roxo para o nó raiz
            node_sizes.append(2000)
        else:
            node_colors.append("#8b5cf6")  # Roxo mais claro para os outros nós
            node_sizes.append(1500 - level * 100)  # Tamanho diminui com o nível
        
        labels[node] = G.nodes[node]["name"]
    
    # Ajustar o tamanho dos nós com base no comprimento do texto
    for node in G.nodes():
        name_length = len(G.nodes[node]["name"])
        idx = list(G.nodes()).index(node)
        node_sizes[idx] = max(1000, name_length * 100)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color="#8b5cf6", width=2, alpha=0.5, arrows=True, arrowsize=15)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="white", font_weight="bold")
    
    plt.axis("off")
    plt.tight_layout()
    
    # Converter o gráfico para imagem
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", transparent=True)
    buf.seek(0)
    plt.close()
    
    return buf

# Função para simular uma resposta da IA (para demonstração)
def simulate_ai_response(topic):
    # Mapas pré-definidos para alguns tópicos comuns
    if topic.lower() == "cachorro":
        return json.dumps({
            "name": "Cachorro",
            "children": [
                {
                    "name": "Raças",
                    "children": [
                        {"name": "Pequeno Porte", "children": [
                            {"name": "Poodle"},
                            {"name": "Chihuahua"},
                            {"name": "Shih Tzu"}
                        ]},
                        {"name": "Médio Porte", "children": [
                            {"name": "Border Collie"},
                            {"name": "Bulldog"},
                            {"name": "Beagle"}
                        ]},
                        {"name": "Grande Porte", "children": [
                            {"name": "Pastor Alemão"},
                            {"name": "Labrador"},
                            {"name": "Golden Retriever"}
                        ]}
                    ]
                },
                {
                    "name": "Cuidados",
                    "children": [
                        {"name": "Alimentação", "children": [
                            {"name": "Ração"},
                            {"name": "Dieta Natural"},
                            {"name": "Suplementos"}
                        ]},
                        {"name": "Saúde", "children": [
                            {"name": "Vacinação"},
                            {"name": "Vermifugação"},
                            {"name": "Check-up Veterinário"}
                        ]},
                        {"name": "Higiene", "children": [
                            {"name": "Banho"},
                            {"name": "Escovação"},
                            {"name": "Corte de Unhas"}
                        ]}
                    ]
                },
                {
                    "name": "Comportamento",
                    "children": [
                        {"name": "Treinamento", "children": [
                            {"name": "Obediência Básica"},
                            {"name": "Socialização"},
                            {"name": "Truques"}
                        ]},
                        {"name": "Linguagem Corporal", "children": [
                            {"name": "Rabo Abanando"},
                            {"name": "Postura de Brincadeira"},
                            {"name": "Sinais de Estresse"}
                        ]},
                        {"name": "Necessidades", "children": [
                            {"name": "Exercício Físico"},
                            {"name": "Estímulo Mental"},
                            {"name": "Afeto e Atenção"}
                        ]}
                    ]
                },
                {
                    "name": "História e Evolução",
                    "children": [
                        {"name": "Origem", "children": [
                            {"name": "Domesticação do Lobo"},
                            {"name": "Seleção Artificial"},
                            {"name": "Coevolução com Humanos"}
                        ]},
                        {"name": "Funções Históricas", "children": [
                            {"name": "Caça"},
                            {"name": "Pastoreio"},
                            {"name": "Guarda"}
                        ]},
                        {"name": "Papel na Sociedade Moderna", "children": [
                            {"name": "Animal de Companhia"},
                            {"name": "Cães de Serviço"},
                            {"name": "Terapia Assistida"}
                        ]}
                    ]
                }
            ]
        })
    else:
        # Estrutura genérica para outros tópicos
        return json.dumps({
            "name": topic,
            "children": [
                {
                    "name": f"Aspectos de {topic}",
                    "children": [
                        {"name": "Característica 1"},
                        {"name": "Característica 2"},
                        {"name": "Característica 3"}
                    ]
                },
                {
                    "name": f"Tipos de {topic}",
                    "children": [
                        {"name": "Tipo 1"},
                        {"name": "Tipo 2"},
                        {"name": "Tipo 3"}
                    ]
                },
                {
                    "name": f"História de {topic}",
                    "children": [
                        {"name": "Origem"},
                        {"name": "Desenvolvimento"},
                        {"name": "Estado Atual"}
                    ]
                },
                {
                    "name": f"Aplicações de {topic}",
                    "children": [
                        {"name": "Uso 1"},
                        {"name": "Uso 2"},
                        {"name": "Uso 3"}
                    ]
                }
            ]
        })

# Função para consultar a API de IA e gerar um mapa de conhecimento
def generate_knowledge_map_with_ai(topic):
    try:
        # Para fins de demonstração, usaremos uma resposta simulada
        # Em produção, substitua isso pela chamada real à API
        ai_response = simulate_ai_response(topic)
        
        # Processar a resposta da IA
        try:
            # Extrair o JSON da resposta
            json_str = ai_response
            knowledge_data = json.loads(json_str)
            
            # Criar um novo mapa de conhecimento
            km = KnowledgeMap(topic)
            km.root = KnowledgeNode.from_dict(knowledge_data)
            
            return km, None
            
        except json.JSONDecodeError as e:
            return None, f"Erro ao processar resposta da IA: {str(e)}"
            
    except Exception as e:
        return None, f"Erro ao gerar mapa de conhecimento com IA: {str(e)}"

# Variável global para armazenar o mapa atual
current_map = None

@app.route('/')
def index():
    global current_map
    return render_template('index.html', map=current_map)

@app.route('/create', methods=['POST'])
def create_map():
    global current_map
    name = request.form.get('name')
    current_map = KnowledgeMap(name)
    return redirect(url_for('index'))

@app.route('/load_example/<theme>')
def load_example(theme):
    global current_map
    current_map = create_example_knowledge_map(theme)
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save_map():
    global current_map
    if not current_map:
        return jsonify({"error": "Nenhum mapa carregado"})
    
    filename = request.form.get('filename')
    if not filename.endswith('.json'):
        filename += '.json'
    
    message = current_map.save(filename)
    return jsonify({"message": message})

@app.route('/load', methods=['POST'])
def load_map():
    global current_map
    filename = request.form.get('filename')
    if not filename.endswith('.json'):
        filename += '.json'
    
    current_map = KnowledgeMap("")
    message = current_map.load(filename)
    return jsonify({"message": message})

@app.route('/add_node', methods=['POST'])
def add_node():
    global current_map
    if not current_map:
        return jsonify({"error": "Nenhum mapa carregado"})
    
    path_str = request.form.get('path', '')
    path = [p.strip() for p in path_str.split(">")] if path_str else []
    node_name = request.form.get('node_name')
    
    success = current_map.add_node(path, node_name)
    if success:
        return jsonify({"message": f"Nó '{node_name}' adicionado com sucesso!"})
    else:
        return jsonify({"error": "Caminho não encontrado"})

@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    global current_map
    if not current_map:
        return jsonify({"error": "Nenhum mapa carregado"})
    
    prompt_type = request.form.get('prompt_type')
    prompt = current_map.generate_prompt(prompt_type)
    return jsonify({"prompt": prompt})

@app.route('/reverse_engineer', methods=['POST'])
def reverse_engineer():
    global current_map
    if not current_map:
        return jsonify({"error": "Nenhum mapa carregado"})
    
    source_text = request.form.get('source_text')
    original_domain = request.form.get('original_domain')
    target_domain = request.form.get('target_domain')
    
    result = current_map.reverse_engineer(source_text, original_domain, target_domain)
    return jsonify({"result": result})

@app.route('/get_map_data')
def get_map_data():
    global current_map
    if not current_map:
        return jsonify({})
    
    return jsonify(current_map.root.to_dict())

@app.route('/get_map_image')
def get_map_image():
    global current_map
    if not current_map:
        return jsonify({"error": "Nenhum mapa carregado"})
    
    buf = render_knowledge_map_image(current_map.root.to_dict())
    return buf.getvalue(), 200, {'Content-Type': 'image/png'}

@app.route('/generate_with_ai', methods=['POST'])
def generate_with_ai():
    global current_map
    
    topic = request.form.get('topic')
    if not topic:
        return jsonify({"error": "Por favor, informe um tópico para pesquisa."})
    
    km, error = generate_knowledge_map_with_ai(topic)
    if error:
        return jsonify({"error": error})
    
    current_map = km
    return jsonify({"message": f"Mapa de conhecimento sobre '{topic}' gerado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)