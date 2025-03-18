"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { KnowledgeMap } from "./components/knowledge-map"
import { KnowledgeList } from "./components/knowledge-list"
import { PromptGenerator } from "./components/prompt-generator"
import { ThemeSelector } from "./components/theme-selector"

export default function Home() {
  const [activeTheme, setActiveTheme] = useState("knowledge-management")

  return (
    <main className="container mx-auto p-4">
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Sistema de Mapeamento de Conhecimentos</CardTitle>
          <CardDescription>
            Ferramenta para mapeamento, organização e engenharia reversa de conhecimentos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <div className="w-full md:w-1/2">
              <ThemeSelector activeTheme={activeTheme} setActiveTheme={setActiveTheme} />
            </div>
            <div className="w-full md:w-1/2">
              <Button className="w-full">Exportar Mapeamento</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="map" className="w-full">
        <TabsList className="grid grid-cols-4 mb-4">
          <TabsTrigger value="map">Mapa Visual</TabsTrigger>
          <TabsTrigger value="list">Lista Hierárquica</TabsTrigger>
          <TabsTrigger value="prompts">Gerador de Prompts</TabsTrigger>
          <TabsTrigger value="reverse">Engenharia Reversa</TabsTrigger>
        </TabsList>

        <TabsContent value="map">
          <KnowledgeMap theme={activeTheme} />
        </TabsContent>

        <TabsContent value="list">
          <KnowledgeList theme={activeTheme} />
        </TabsContent>

        <TabsContent value="prompts">
          <PromptGenerator theme={activeTheme} />
        </TabsContent>

        <TabsContent value="reverse">
          <Card>
            <CardHeader>
              <CardTitle>Engenharia Reversa de Conhecimento</CardTitle>
              <CardDescription>Analise estruturas existentes e reconstrua para novos domínios</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <label className="block mb-2 text-sm font-medium">Fonte de Conhecimento</label>
                <Textarea
                  placeholder="Cole aqui o texto ou estrutura de conhecimento que deseja analisar..."
                  className="min-h-[200px]"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block mb-2 text-sm font-medium">Domínio Original</label>
                  <Input defaultValue="Gestão do Conhecimento" />
                </div>
                <div>
                  <label className="block mb-2 text-sm font-medium">Novo Domínio</label>
                  <Input defaultValue="TDAH" />
                </div>
              </div>

              <Button className="w-full">Realizar Engenharia Reversa</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  )
}

