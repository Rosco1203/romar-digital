// RoMar Digital website chat assistant (Retell website widget).
// The Retell PUBLIC key is client-side by design; it is restricted to allowed domains in the Retell dashboard.
// The widget labels switch to Spanish on pages whose <html lang> is "es" (the /es/ page).
(function () {
  var es = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;
  var s = document.createElement('script');
  s.id = 'retell-widget';
  s.src = 'https://dashboard.retellai.com/retell-widget-v2.js';
  s.setAttribute('data-public-key', 'public_key_d6159c4a087e1666df7e9');
  s.setAttribute('data-agent-id', 'agent_82531adf7fb562e6d4d505f420');
  s.setAttribute('data-title', es ? 'Chatee con RoMar Digital' : 'Chat with RoMar Digital');
  s.setAttribute('data-color', '#2563eb');
  s.setAttribute('data-bot-name', es ? 'Asistente de IA de RoMar Digital' : 'RoMar Digital AI Assistant');
  s.setAttribute('data-fab-text', es ? 'Pregúntenos' : 'Ask us anything');
  s.setAttribute('data-show-ai-popup', 'false');
  document.head.appendChild(s);
})();
