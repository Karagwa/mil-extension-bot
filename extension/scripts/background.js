// A variable to store the results from our API, so the popup can access them.
let analysisResults = null;

// The localtunnel domain changes each time you restart the localtunnel command (lt --port 8000).
// Update this public URL each time you restart localtunnel.
const API_BASE_URL = "https://milbot.loca.lt";
// Replace with your actual tunnel password from: curl https://loca.lt/mytunnelpassword
const TUNNEL_PASSWORD = "41.210.143.237"; 

// Listen for a message from the content script.
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'analyzeContent') {
    // Handle async operation properly
    (async () => {
      try {
        // Step 1: Call the analyze endpoint with url, title, and content
        const analyzeHeaders = {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true'
        };
        if (TUNNEL_PASSWORD) analyzeHeaders['tunnel-password'] = TUNNEL_PASSWORD;

        const analyzeResponse = await fetch(`${API_BASE_URL}/analyze/`, {
          method: 'POST',
          headers: analyzeHeaders,
          body: JSON.stringify({
            url: message.data.url,
            title: message.data.title,
            content: message.data.text
          })
        });

        if (!analyzeResponse.ok) {
          // Log response details for debugging
          const responseText = await analyzeResponse.text();
          console.error(`Analyze API error: ${analyzeResponse.status} - ${responseText}`);
          throw new Error(`HTTP error! status: ${analyzeResponse.status}`);
        }
        const analysisData = await analyzeResponse.json();

        // Storing all the results in the global variable for use when needed.
        analysisResults = {
          title: message.data.title,
          url: message.data.url,
          analysis: analysisData
        };

        console.log('API calls successful:', analysisResults);

        // Notify any open popup that results are ready
        chrome.runtime.sendMessage({ action: 'resultsReady', data: analysisResults });

      } catch (error) {
        console.error('Error during API calls:', error);
        analysisResults = {
          error: `Failed to connect to the API: ${error.message}`
        };
      }
    })();
    
    return true; // Keeps the messaging channel open
  }

  // This listener handles requests from the popup to get the results.
  if (message.action === 'getResults') {
    sendResponse(analysisResults);
    return true; // Keeps the messaging channel open for async response
  }

  // Handle feedback submission from the popup
  if (message.action === 'logFeedback') {
    (async () => {
      try {
        const fbHeaders = {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true'
        };
        if (TUNNEL_PASSWORD) fbHeaders['tunnel-password'] = TUNNEL_PASSWORD;
        const fbResponse = await fetch(`${API_BASE_URL}/feedback/`, {
          method: 'POST',
          headers: fbHeaders,
          body: JSON.stringify({
            analysis_id: message.data.analysis_id,
            helpful: message.data.helpful,
            note: null,
            source: 'extension'
          })
        });
        if (!fbResponse.ok) {
          const txt = await fbResponse.text();
          console.error(`Feedback API error: ${fbResponse.status} - ${txt}`);
          sendResponse({ ok: false });
          return;
        }
        sendResponse({ ok: true });
      } catch (e) {
        console.error('Feedback submit failed:', e);
        sendResponse({ ok: false });
      }
    })();
    return true;
  }
});