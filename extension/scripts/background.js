// A variable to store the results from our API, so the popup can access them.
let analysisResults = null;

// The ngrok domain changes each time you restart the ngrok command (ngrok http 8000).
// Update this public URL each time you restart ngrok.
const API_BASE_URL = "https://major-streets-act.loca.lt";

// Listen for a message from the content script.
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === 'analyzeContent') {
    try {
      // Step 1: Calling the analyze endpoint with the article text
      const analyzeResponse = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: message.data.text
        })
      });

      if (!analyzeResponse.ok) {
        throw new Error(`HTTP error! status: ${analyzeResponse.status}`);
      }
      const analysisData = await analyzeResponse.json();

      // Step 2: Calling the feedback/links endpoint with the extracted links
      const linksResponse = await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          links: message.data.links
        })
      });
      if (!linksResponse.ok) {
        throw new Error(`HTTP error! status: ${linksResponse.status}`);
      }
      const linksData = await linksResponse.json();

      // Storing all the results in the global variable for use when needed.
      analysisResults = {
        title: message.data.title,
        url: message.data.url,
        analysis: analysisData,
        links: linksData
      };

    } catch (error) {
      console.error('Error during API calls:', error);
      analysisResults = {
        error: "Failed to connect to the API."
      };
    }
  }

  // This listener handles requests from the popup to get the results.
  // It's a separate message to avoid confusion.
  if (message.action === 'getResults') {
    sendResponse(analysisResults);
    return true; // Keeps the messaging channel open for async response
  }
});