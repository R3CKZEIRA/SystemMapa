interface KnowledgeNode {
  id: string
  name: string
  children?: KnowledgeNode[]
}

// Dados de exemplo para Gestão do Conhecimento
const knowledgeManagementStructure: KnowledgeNode = {
  id: "root",
  name: "Gestão do Conhecimento",
  children: [
    {
      id: "concepts",
      name: "Conceitos Fundamentais",
      children: [
        { id: "tacit", name: "Conhecimento Tácito" },
        { id: "explicit", name: "Conhecimento Explícito" },
        { id: "conversion", name: "Conversão de Conhecimento" },
      ],
    },
    {
      id: "processes",
      name: "Processos",
      children: [
        { id: "creation", name: "Criação de Conhecimento" },
        { id: "storage", name: "Armazenamento" },
        { id: "sharing", name: "Compartilhamento" },
        { id: "application", name: "Aplicação" },
      ],
    },
    {
      id: "tools",
      name: "Ferramentas",
      children: [
        { id: "km-systems", name: "Sistemas de GC" },
        { id: "communities", name: "Comunidades de Prática" },
        { id: "taxonomies", name: "Taxonomias e Ontologias" },
      ],
    },
    {
      id: "metrics",
      name: "Métricas e Avaliação",
      children: [
        { id: "roi", name: "ROI do Conhecimento" },
        { id: "maturity", name: "Modelos de Maturidade" },
      ],
    },
  ],
}

// Dados de exemplo para TDAH
const tdahStructure: KnowledgeNode = {
  id: "root",
  name: "TDAH",
  children: [
    {
      id: "concepts",
      name: "Conceitos Fundamentais",
      children: [
        { id: "attention", name: "Déficit de Atenção" },
        { id: "hyperactivity", name: "Hiperatividade" },
        { id: "impulsivity", name: "Impulsividade" },
      ],
    },
    {
      id: "diagnosis",
      name: "Diagnóstico",
      children: [
        { id: "criteria", name: "Critérios Diagnósticos" },
        { id: "assessment", name: "Avaliação Clínica" },
        { id: "differential", name: "Diagnóstico Diferencial" },
      ],
    },
    {
      id: "treatment",
      name: "Tratamento",
      children: [
        { id: "medication", name: "Medicação" },
        { id: "therapy", name: "Terapia Comportamental" },
        { id: "coaching", name: "Coaching para TDAH" },
      ],
    },
    {
      id: "management",
      name: "Gestão Diária",
      children: [
        { id: "strategies", name: "Estratégias de Organização" },
        { id: "tools", name: "Ferramentas de Apoio" },
      ],
    },
  ],
}

export function getKnowledgeStructure(theme: string): KnowledgeNode {
  switch (theme) {
    case "tdah":
      return tdahStructure
    case "knowledge-management":
    default:
      return knowledgeManagementStructure
  }
}

