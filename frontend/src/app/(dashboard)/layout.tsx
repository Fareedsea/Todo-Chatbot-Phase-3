// T033: Dashboard layout with NavBar

import NavBar from '@/components/layout/NavBar';
import ChatbotIcon from '@/chat/ChatbotIcon';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      {/* AI Chatbot - Always visible for authenticated users */}
      <ChatbotIcon />
    </div>
  );
}
