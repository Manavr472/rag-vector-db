'use client'

import { useState } from 'react'
import { Send, Moon, Sun, Bot, User, Building2, Heart } from 'lucide-react'
import { useTheme } from './components/ThemeProvider'

interface Message {
  id: string
  content: string
  sender: 'user' | 'bot'
  timestamp: Date
  botType?: 'business' | 'healthcare'
}

export default function Home() {
  const { theme, toggleTheme } = useTheme()
  // Separate message histories for each bot
  const [businessMessages, setBusinessMessages] = useState<Message[]>([])
  const [healthcareMessages, setHealthcareMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedBot, setSelectedBot] = useState<'business' | 'healthcare'>('business')

  // Get current messages based on selected bot
  const currentMessages = selectedBot === 'business' ? businessMessages : healthcareMessages
  const setCurrentMessages = selectedBot === 'business' ? setBusinessMessages : setHealthcareMessages

  // Clear current bot's conversation history
  const clearCurrentHistory = () => {
    setCurrentMessages([])
  }

  const sendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
      botType: selectedBot
    }

    // Add message to the current bot's history
    setCurrentMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Call the Vercel serverless API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          botType: selectedBot
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response || "I'm sorry, I couldn't process that request.",
        sender: 'bot',
        timestamp: new Date(),
        botType: selectedBot
      }

      // Add bot response to the current bot's history
      setCurrentMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('API Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting right now. Please try again later.",
        sender: 'bot',
        timestamp: new Date(),
        botType: selectedBot
      }
      // Add error message to the current bot's history
      setCurrentMessages(prev => [...prev, errorMessage])
    }

    setIsLoading(false)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getBotIcon = (botType: 'business' | 'healthcare') => {
    return botType === 'business' ? Building2 : Heart
  }

  const getBotColor = (botType: 'business' | 'healthcare') => {
    return botType === 'business' 
      ? 'text-blue-600 dark:text-blue-400' 
      : 'text-green-600 dark:text-green-400'
  }

  // Enhanced function to parse and format bot responses
  const parseResponse = (text: string) => {
    if (!text) return text

    // Split by lines first to handle line breaks
    const lines = text.split('\n')
    
    return lines.map((line, lineIndex) => {
      const trimmedLine = line.trim()
      
      // Handle empty lines
      if (!trimmedLine) return <br key={lineIndex} />
      
      // Handle headers (### Header)
      const headerMatch = trimmedLine.match(/^(#{1,3})\s+(.+)$/)
      if (headerMatch) {
        const level = headerMatch[1].length
        const content = headerMatch[2]
        const HeaderTag = `h${Math.min(level + 2, 6)}` as keyof JSX.IntrinsicElements
        return (
          <HeaderTag key={lineIndex} className="font-semibold text-gray-900 dark:text-white mb-2 mt-3">
            {content}
          </HeaderTag>
        )
      }
      
      // Handle medical disclaimer specially
      if (trimmedLine.includes('⚠️') && (trimmedLine.includes('Medical Disclaimer') || trimmedLine.includes('educational purposes'))) {
        const cleanText = trimmedLine.replace(/⚠️\s*\*\*|\*\*/g, '').replace('Medical Disclaimer:', '').trim()
        return (
          <div key={lineIndex} className="mt-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <div className="flex items-start gap-2">
              <span className="text-yellow-600 dark:text-yellow-400 text-sm">⚠️</span>
              <div className="text-xs text-yellow-800 dark:text-yellow-200 font-medium">
                <strong>Medical Disclaimer:</strong> {cleanText}
              </div>
            </div>
          </div>
        )
      }
      
      // Parse inline formatting within each line
      const parts: { type: string; content: string; id: number }[] = []
      let currentText = trimmedLine
      let partIndex = 0
      
      // First pass: Handle bold text (**text**) - need to do this before italic to avoid conflicts
      currentText = currentText.replace(/\*\*(.*?)\*\*/g, (match, content) => {
        const placeholder = `__BOLD_${partIndex}__`
        parts.push({ type: 'bold', content, id: partIndex })
        partIndex++
        return placeholder
      })
      
      // Second pass: Handle italic/emphasis (*text*) - only single asterisks not already processed
      currentText = currentText.replace(/(?<!\*)(\*)(?!\*)([^*]+?)(\*)(?!\*)/g, (match, start, content, end) => {
        const placeholder = `__ITALIC_${partIndex}__`
        parts.push({ type: 'italic', content, id: partIndex })
        partIndex++
        return placeholder
      })
      
      // Handle bullet points more flexibly (*, •, -, or numbers)
      const bulletPatterns = [
        /^[\s]*\*\s+(.+)$/, // * bullet
        /^[\s]*[•]\s+(.+)$/, // • bullet
        /^[\s]*[-]\s+(.+)$/, // - bullet
        /^[\s]*\d+\.\s+(.+)$/ // numbered list
      ]
      
      let isBulletPoint = false
      let bulletContent = currentText
      let bulletSymbol = '•'
      
      for (const pattern of bulletPatterns) {
        const match = currentText.match(pattern)
        if (match) {
          isBulletPoint = true
          bulletContent = match[1]
          // Determine bullet symbol based on original pattern
          if (trimmedLine.includes('*')) bulletSymbol = '•'
          else if (trimmedLine.includes('•')) bulletSymbol = '•'
          else if (trimmedLine.includes('-')) bulletSymbol = '•'
          else if (/^\d+\./.test(trimmedLine)) {
            const numberMatch = trimmedLine.match(/^(\d+)\.\s/)
            bulletSymbol = numberMatch ? `${numberMatch[1]}.` : '•'
          }
          break
        }
      }
      
      // Split text by placeholders and create elements
      const textParts = bulletContent.split(/(__(?:BOLD|ITALIC)_\d+__)/g)
      
      const formattedContent = textParts.map((part, index) => {
        const boldMatch = part.match(/^__BOLD_(\d+)__$/)
        const italicMatch = part.match(/^__ITALIC_(\d+)__$/)
        
        if (boldMatch) {
          const boldPart = parts.find(p => p.id === parseInt(boldMatch[1]))
          return <strong key={`${lineIndex}-${index}`} className="font-semibold text-gray-900 dark:text-white">{boldPart?.content}</strong>
        } else if (italicMatch) {
          const italicPart = parts.find(p => p.id === parseInt(italicMatch[1]))
          return <em key={`${lineIndex}-${index}`} className="italic text-gray-700 dark:text-gray-300">{italicPart?.content}</em>
        } else {
          return part
        }
      })
      
      if (isBulletPoint) {
        return (
          <div key={lineIndex} className="flex items-start gap-2 ml-4 my-1">
            <span className="text-blue-600 dark:text-blue-400 mt-0.5 font-medium text-sm min-w-[1rem]">
              {bulletSymbol}
            </span>
            <span className="flex-1">{formattedContent}</span>
          </div>
        )
      }
      
      return <div key={lineIndex} className="my-1 leading-relaxed">{formattedContent}</div>
    })
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <Bot className="w-6 h-6 text-primary-600" />
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              AI QA Bot Collection
            </h1>
          </div>
          
          {/* Bot Selector */}
          <div className="flex items-center gap-2">
            <div className="flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
              <button
                onClick={() => setSelectedBot('business')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  selectedBot === 'business'
                    ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                <Building2 className="w-4 h-4" />
                <span>Business</span>
                {businessMessages.length > 0 && (
                  <span className="ml-1 px-1.5 py-0.5 text-xs bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded-full">
                    {Math.ceil(businessMessages.filter(m => m.sender === 'user').length)}
                  </span>
                )}
              </button>
              <button
                onClick={() => setSelectedBot('healthcare')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  selectedBot === 'healthcare'
                    ? 'bg-white dark:bg-gray-600 text-green-600 dark:text-green-400 shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                <Heart className="w-4 h-4" />
                <span>Healthcare</span>
                {healthcareMessages.length > 0 && (
                  <span className="ml-1 px-1.5 py-0.5 text-xs bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-300 rounded-full">
                    {Math.ceil(healthcareMessages.filter(m => m.sender === 'user').length)}
                  </span>
                )}
              </button>
            </div>
            
            {/* Clear History Button */}
            {currentMessages.length > 0 && (
              <button
                onClick={clearCurrentHistory}
                className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title={`Clear ${selectedBot} chat history`}
              >
                Clear
              </button>
            )}
            
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-4xl mx-auto flex flex-col">
          {/* Bot History Indicator */}
          {(businessMessages.length > 0 || healthcareMessages.length > 0) && (
            <div className="px-4 py-2 border-b border-gray-100 dark:border-gray-800">
              <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
                Viewing {selectedBot === 'business' ? 'Business' : 'Healthcare'} conversation history 
                {currentMessages.length > 0 && (
                  <span className="ml-1">
                    ({Math.ceil(currentMessages.filter(m => m.sender === 'user').length)} questions)
                  </span>
                )}
              </div>
            </div>
          )}
          
          <div className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin transition-all duration-300 ease-in-out">
            {currentMessages.length === 0 ? (
              <div className="text-center py-12">
                <div className={`inline-flex p-4 rounded-full mb-4 ${getBotColor(selectedBot)} bg-gray-100 dark:bg-gray-800`}>
                  {(() => {
                    const IconComponent = getBotIcon(selectedBot)
                    return <IconComponent className="w-8 h-8" />
                  })()}
                </div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {selectedBot === 'business' ? 'Business Assistant' : 'Healthcare Assistant'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
                  {selectedBot === 'business' 
                    ? 'Ask me about services, pricing, company information, and business inquiries.'
                    : 'Ask me about health topics, symptoms, treatments, and medical information. (Educational purposes only)'
                  }
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {currentMessages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'} message-enter`}
                  >
                    {message.sender === 'bot' && (
                      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                        message.botType === 'business' 
                          ? 'bg-blue-100 dark:bg-blue-900' 
                          : 'bg-green-100 dark:bg-green-900'
                      }`}>
                        {(() => {
                          const IconComponent = getBotIcon(message.botType || selectedBot)
                          return <IconComponent className={`w-4 h-4 ${getBotColor(message.botType || selectedBot)}`} />
                        })()}
                      </div>
                    )}
                    
                    <div className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-2 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700'
                    }`}>
                      <div className="text-sm space-y-1">
                        {message.sender === 'bot' ? parseResponse(message.content) : message.content}
                      </div>
                    </div>

                    {message.sender === 'user' && (
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
                        <User className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex gap-3 justify-start message-enter">
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      selectedBot === 'business' 
                        ? 'bg-blue-100 dark:bg-blue-900' 
                        : 'bg-green-100 dark:bg-green-900'
                    }`}>
                      {(() => {
                        const IconComponent = getBotIcon(selectedBot)
                        return <IconComponent className={`w-4 h-4 ${getBotColor(selectedBot)}`} />
                      })()}
                    </div>
                    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-4 py-2 rounded-lg">
                      <div className="typing-indicator">
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder={`Ask the ${selectedBot} assistant...`}
                  className="w-full px-4 py-2 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  rows={1}
                  style={{ minHeight: '40px', maxHeight: '120px' }}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1.5 text-gray-400 hover:text-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
