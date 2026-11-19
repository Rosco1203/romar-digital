// RoMar Digital website chat assistant (Retell website widget).
// The Retell PUBLIC key is client-side by design; it is restricted to allowed domains in the Retell dashboard.
// On the Spanish page the widget also passes dynamic variables so the agent's first message (begin_message = {{greeting}}) is in Spanish;
// on the English page nothing is passed and the agent's default (English) greeting is used.
// The widget labels switch to Spanish on pages whose <html lang> is "es" (the /es/ page).
(function () {
  var es = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;
  // Keep a separate chat session per page language. The Retell widget stores its chat id, history and chat list in
  // localStorage keys shared by / and /es/, so without this a Spanish chat would continue on the English page (and the
  // other way round). When the language changes, park the current session under its own language and restore the saved
  // session for the new language, or start fresh (which shows the right greeting).
  try {
    var lang = es ? 'es' : 'en';
    var KEYS = ['LS_CHAT_ID', 'LS_CHAT_HISTORY', 'LS_CHAT_LIST'];
    var cur = localStorage.getItem('romar_chat_lang');
    if (!cur) {
      // Session saved before this fix: tell the language from the greeting it starts with.
      var raw = (localStorage.getItem('LS_CHAT_HISTORY') || '') + (localStorage.getItem('LS_CHAT_LIST') || '');
      cur = raw.indexOf('Hola, soy el asistente') !== -1 ? 'es' : 'en';
    }
    if (cur !== lang) {
      var parked = {};
      KEYS.forEach(function (k) { var v = localStorage.getItem(k); if (v !== null) parked[k] = v; });
      localStorage.setItem('romar_chat_session_' + cur, JSON.stringify(parked));
      KEYS.forEach(function (k) { localStorage.removeItem(k); });
      var saved = localStorage.getItem('romar_chat_session_' + lang);
      if (saved) {
        var restored = JSON.parse(saved);
        Object.keys(restored).forEach(function (k) { localStorage.setItem(k, restored[k]); });
        localStorage.removeItem('romar_chat_session_' + lang);
      }
    }
    localStorage.setItem('romar_chat_lang', lang);
  } catch (e) { /* storage unavailable: widget behaves as before */ }
  var s = document.createElement('script');
  s.id = 'retell-widget';
  s.src = 'https://dashboard.retellai.com/retell-widget-v2.js';
  s.setAttribute('data-public-key', 'public_key_d6159c4a087e1666df7e9');
  s.setAttribute('data-agent-id', 'agent_82531adf7fb562e6d4d505f420');
  s.setAttribute('data-title', es ? 'Chatee con RoMar Digital' : 'Chat with RoMar Digital');
  s.setAttribute('data-color', '#C9883A');
  s.setAttribute('data-bot-name', es ? 'Asistente de IA de RoMar Digital' : 'RoMar Digital AI Assistant');
  s.setAttribute('data-fab-text', es ? 'Pregúntenos' : 'Ask us anything');
  s.setAttribute('data-show-ai-popup', 'false');
  if (es) {
    s.setAttribute('data-dynamic', JSON.stringify({
      page_language: 'es',
      greeting: "Hola, soy el asistente de IA de RoMar Digital (un asistente automatizado, no una persona). Puedo responder preguntas sobre nuestra recepcionista de voz con IA, la gestión de reseñas, sitios web, chatbots, paquetes y precios, y orientarle a la página correcta. También puedo ayudarle en inglés. ¿En qué puedo ayudarle?"
    }));
  }
  document.head.appendChild(s);
})();
