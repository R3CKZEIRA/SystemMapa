"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChevronRight, ChevronDown, Plus, Edit, Trash } from "lucide-react"
import { getKnowledgeStructure } from "../utils/knowledge-data"

interface KnowledgeListProps {
  theme: string
}

interface KnowledgeNode {
  id: string
  name: string
  children?: KnowledgeNode[]
}

export function KnowledgeList({ theme }: KnowledgeListProps) {
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({
    root: true,
    concepts: true,
  })

  const toggleNode = (id: string) => {
    setExpandedNodes((prev) => ({
      ...prev,
      [id]: !prev[id],
    }))
  }

  const structure = getKnowledgeStructure(theme)

  const renderNode = (node: KnowledgeNode, depth = 0) => {
    const isExpanded = expandedNodes[node.id] || false
    const hasChildren = node.children && node.children.length > 0

    return (
      <div key={node.id}>
        <div
          className={`
            flex items-center p-2 hover:bg-gray-100 rounded-md
            ${depth === 0 ? "bg-purple-100" : ""}
          `}
          style={{ paddingLeft: `${depth * 20 + 8}px` }}
        >
          {hasChildren ? (
            <button onClick={() => toggleNode(node.id)} className="mr-1 text-gray-500 hover:text-gray-700">
              {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
            </button>
          ) : (
            <div className="w-5" />
          )}

          <span className="flex-grow">{node.name}</span>

          <div className="flex gap-1">
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <Plus className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <Edit className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <Trash className="h-3 w-3" />
            </Button>
          </div>
        </div>

        {isExpanded && hasChildren && <div>{node.children!.map((child) => renderNode(child, depth + 1))}</div>}
      </div>
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Lista Hierárquica: {theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"}</CardTitle>
        <div className="flex items-center gap-2">
          <Input placeholder="Buscar..." className="max-w-xs" />
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Novo Item
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="border rounded-lg p-2 bg-white">{renderNode(structure)}</div>
      </CardContent>
    </Card>
  )
}

