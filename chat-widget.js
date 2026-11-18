// RoMar Digital website chat assistant (Retell website widget).
// The Retell PUBLIC key is client-side by design; it is restricted to allowed domains in the Retell dashboard.
// On the Spanish page the widget also passes dynamic variables so the agent's first message (begin_message = {{greeting}}) is in Spanish;
// on the English page nothing is passed and the agent's default (English) greeting is used.
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
  if (es) {
    s.setAttribute('data-dynamic', JSON.stringify({
      page_language: 'es',
      greeting: "Hola, soy el asistente de IA de RoMar Digital (un asistente automatizado, no una persona). Puedo responder preguntas sobre nuestra recepcionista de voz con IA, sitios web, chatbots, paquetes y precios, y orientarle a la página correcta. También puedo ayudarle en inglés. ¿En qué puedo ayudarle?"
    }));
  }
  document.head.appendChild(s);
})();
