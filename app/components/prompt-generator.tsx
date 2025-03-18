"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { getPromptTemplates } from "../utils/prompt-templates"

interface PromptGeneratorProps {
  theme: string
}

export function PromptGenerator({ theme }: PromptGeneratorProps) {
  const [promptType, setPromptType] = useState("map")
  const [generatedPrompt, setGeneratedPrompt] = useState("")

  const promptTemplates = getPromptTemplates(theme)

  const generatePrompt = () => {
    const template = promptTemplates.find((t) => t.id === promptType)
    if (template) {
      setGeneratedPrompt(template.template)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedPrompt)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Gerador de Prompts</CardTitle>
        <CardDescription>
          Gere prompts predefinidos para mapear conhecimentos sobre{" "}
          {theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block mb-2 text-sm font-medium">Tipo de Prompt</label>
            <Select value={promptType} onValueChange={setPromptType}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o tipo de prompt" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="map">Mapeamento de Conceitos</SelectItem>
                <SelectItem value="structure">Estruturação Hierárquica</SelectItem>
                <SelectItem value="reverse">Engenharia Reversa</SelectItem>
                <SelectItem value="adapt">Adaptação para Novo Domínio</SelectItem>
                <SelectItem value="validate">Validação de Conhecimento</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-end">
            <Button onClick={generatePrompt} className="w-full">
              Gerar Prompt
            </Button>
          </div>
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium">Prompt Gerado</label>
          <Textarea
            value={generatedPrompt}
            onChange={(e) => setGeneratedPrompt(e.target.value)}
            className="min-h-[200px]"
            placeholder="O prompt gerado aparecerá aqui..."
          />
        </div>

        <div className="flex justify-end">
          <Button onClick={copyToClipboard} variant="outline">
            Copiar para Área de Transferência
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

