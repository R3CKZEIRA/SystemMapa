"use client"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface ThemeSelectorProps {
  activeTheme: string
  setActiveTheme: (theme: string) => void
}

export function ThemeSelector({ activeTheme, setActiveTheme }: ThemeSelectorProps) {
  return (
    <div>
      <label className="block mb-2 text-sm font-medium">Tema de Conhecimento</label>
      <Select value={activeTheme} onValueChange={setActiveTheme}>
        <SelectTrigger>
          <SelectValue placeholder="Selecione o tema" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="knowledge-management">Gestão do Conhecimento</SelectItem>
          <SelectItem value="tdah">TDAH</SelectItem>
          <SelectItem value="custom">Personalizado</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )
}

