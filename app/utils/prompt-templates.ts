interface PromptTemplate {
  id: string
  name: string
  template: string
}

export function getPromptTemplates(theme: string): PromptTemplate[] {
  // Templates base para qualquer tema
  const baseTemplates: PromptTemplate[] = [
    {
      id: "map",
      name: "Mapeamento de Conceitos",
      template: `Mapeie os principais conceitos relacionados a ${theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"}, organizando-os em categorias e subcategorias. Para cada conceito, forneça uma breve definição e sua relevância no contexto geral.`,
    },
    {
      id: "structure",
      name: "Estruturação Hierárquica",
      template: `Crie uma estrutura hierárquica para organizar o conhecimento sobre ${theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"}, começando com os conceitos mais amplos e descendo até os mais específicos. Utilize uma estrutura de árvore com no máximo 3 níveis de profundidade.`,
    },
    {
      id: "reverse",
      name: "Engenharia Reversa",
      template: `Analise a seguinte estrutura de conhecimento e identifique os padrões, princípios e metodologias utilizados para organizá-la. Em seguida, explique como esses mesmos princípios poderiam ser aplicados a um domínio diferente.`,
    },
    {
      id: "adapt",
      name: "Adaptação para Novo Domínio",
      template: `Pegue a estrutura de conhecimento sobre ${theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"} e adapte-a para o domínio de ${theme === "knowledge-management" ? "TDAH" : "Gestão do Conhecimento"}, mantendo a mesma organização hierárquica e princípios estruturais, mas substituindo os conceitos específicos.`,
    },
    {
      id: "validate",
      name: "Validação de Conhecimento",
      template: `Avalie a seguinte estrutura de conhecimento sobre ${theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"} e identifique possíveis lacunas, inconsistências ou áreas que poderiam ser expandidas. Sugira melhorias específicas para tornar a estrutura mais completa e coerente.`,
    },
  ]

  // Templates específicos para Gestão do Conhecimento
  if (theme === "knowledge-management") {
    return [
      ...baseTemplates,
      {
        id: "km-processes",
        name: "Processos de GC",
        template:
          "Descreva em detalhes os principais processos de Gestão do Conhecimento (criação, armazenamento, compartilhamento, aplicação) e como eles se inter-relacionam em um ciclo contínuo. Para cada processo, identifique ferramentas e técnicas específicas que podem ser utilizadas.",
      },
    ]
  }

  // Templates específicos para TDAH
  if (theme === "tdah") {
    return [
      ...baseTemplates,
      {
        id: "tdah-strategies",
        name: "Estratégias para TDAH",
        template:
          "Elabore um conjunto abrangente de estratégias para lidar com os desafios do TDAH em diferentes contextos (acadêmico, profissional, pessoal). Organize as estratégias por tipo de desafio (atenção, hiperatividade, impulsividade) e por ambiente de aplicação.",
      },
    ]
  }

  return baseTemplates
}

