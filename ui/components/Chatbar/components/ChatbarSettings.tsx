import { useContext } from 'react';

import HomeContext from '@/pages/api/home/home.context';

import ChatbarContext from '../Chatbar.context';
import { ClearConversations } from './ClearConversations';
import { ModeSelector } from './ModeSelector';

export const ChatbarSettings = () => {
  const {
    state: { conversations },
  } = useContext(HomeContext);

  const { handleClearConversations } = useContext(ChatbarContext);

  return (
    <div className="flex flex-col">
      <div className="flex flex-col items-center space-y-1 border-t border-white/20 pt-1 text-sm">
        {conversations.length > 0 ? (
          <ClearConversations onClearConversations={handleClearConversations} />
        ) : null}
      </div>
      <ModeSelector />
    </div>
  );
};
