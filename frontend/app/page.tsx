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

type BotType = 'business' | 'healthcare'

export default function Home() {
  const { theme, toggleTheme } = useTheme()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedBot, setSelectedBot] = useState<BotType>('business')

  const sendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
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

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('API Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting right now. Please try again later.",
        sender: 'bot',
        timestamp: new Date(),
        botType: selectedBot
      }
      setMessages(prev => [...prev, errorMessage])
    }

    setIsLoading(false)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getBotIcon = (botType: BotType) => {
    return botType === 'business' ? Building2 : Heart
  }

  const getBotColor = (botType: BotType) => {
    return botType === 'business' 
      ? 'text-blue-600 dark:text-blue-400' 
      : 'text-green-600 dark:text-green-400'
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
                Business
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
                Healthcare
              </button>
            </div>
            
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
          <div className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin">
            {messages.length === 0 ? (
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
                {messages.map((message) => (
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
                      <p className="text-sm whitespace-pre-wrap">{message.content}</p>
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
