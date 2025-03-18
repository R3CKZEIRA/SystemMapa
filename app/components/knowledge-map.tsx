"use client"

import { useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { PlusCircle, ZoomIn, ZoomOut, Download } from "lucide-react"
import { getKnowledgeStructure } from "../utils/knowledge-data"

interface KnowledgeMapProps {
  theme: string
}

export function KnowledgeMap({ theme }: KnowledgeMapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Reset canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Get knowledge structure based on selected theme
    const structure = getKnowledgeStructure(theme)

    // Draw the knowledge map
    drawKnowledgeMap(ctx, structure, canvas.width / 2, 50, canvas.width * 0.8)
  }, [theme])

  const drawKnowledgeMap = (
    ctx: CanvasRenderingContext2D,
    structure: any,
    x: number,
    y: number,
    width: number,
    depth = 0,
  ) => {
    // Draw node
    ctx.fillStyle = depth === 0 ? "#7c3aed" : "#8b5cf6"
    ctx.strokeStyle = "#4c1d95"
    ctx.lineWidth = 2

    const nodeHeight = 40
    const nodeWidth = Math.min(width, 200)

    ctx.beginPath()
    ctx.roundRect(x - nodeWidth / 2, y, nodeWidth, nodeHeight, 8)
    ctx.fill()
    ctx.stroke()

    // Draw text
    ctx.fillStyle = "#ffffff"
    ctx.font = "14px sans-serif"
    ctx.textAlign = "center"
    ctx.textBaseline = "middle"
    ctx.fillText(structure.name, x, y + nodeHeight / 2, nodeWidth - 20)

    // Draw children
    if (structure.children && structure.children.length > 0) {
      const childrenWidth = width * 0.9
      const childWidth = childrenWidth / structure.children.length

      structure.children.forEach((child: any, index: number) => {
        const childX = x - childrenWidth / 2 + childWidth / 2 + index * childWidth
        const childY = y + nodeHeight + 40

        // Draw connection line
        ctx.strokeStyle = "#8b5cf6"
        ctx.beginPath()
        ctx.moveTo(x, y + nodeHeight)
        ctx.lineTo(childX, childY)
        ctx.stroke()

        // Draw child node
        drawKnowledgeMap(ctx, child, childX, childY, childWidth * 0.9, depth + 1)
      })
    }
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>
          Mapa de Conhecimento: {theme === "knowledge-management" ? "Gestão do Conhecimento" : "TDAH"}
        </CardTitle>
        <div className="flex gap-2">
          <Button variant="outline" size="icon">
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative border rounded-lg overflow-auto bg-white">
          <canvas ref={canvasRef} width={1000} height={600} className="w-full"></canvas>

          <Button variant="outline" size="sm" className="absolute bottom-4 right-4">
            <PlusCircle className="h-4 w-4 mr-2" />
            Adicionar Nó
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

