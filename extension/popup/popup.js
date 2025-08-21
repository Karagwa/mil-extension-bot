document.addEventListener('DOMContentLoaded', () => {
  const loadingSpinner = document.getElementById('loading-spinner');
  const resultsDiv = document.getElementById('analysis-results');

  function renderResults(response) {
    loadingSpinner.style.display = 'none';
    resultsDiv.style.display = 'block';

    if (!response || response.error) {
      const errorMsg = response?.error ? String(response.error) : 'Could not retrieve analysis results. Please check your network connection.';
      document.getElementById('analysis-results').innerHTML = `<p>Error: ${errorMsg}</p>`;
      return;
    }

    document.getElementById('article-title').textContent = response.title || '';
    // API returns AnalyzeOut: label, score, tips, model_name, created_at, analysis_id
    document.getElementById('credibility-score').textContent = String(response.analysis?.score ?? '');

    if (response.analysis?.label === 'misleading') {
      document.getElementById('ai-warning').style.display = 'block';
    }

    // No links endpoint in backend; hide list
    document.getElementById('false-links-list').style.display = 'none';

    // stash analysis_id for feedback later
    window.__analysis_id = response.analysis?.analysis_id;

    // Back compat in case older background provided flag
    if (response.analysis?.isAiGenerated) {
      document.getElementById('ai-warning').style.display = 'block';
    }
    
  }

  // Listen for background notification when results are ready
  chrome.runtime.onMessage.addListener((message) => {
    if (message?.action === 'resultsReady') {
      renderResults(message.data);
    }
  });

  // Try to get cached results immediately; if not available, poll briefly
  const POLL_INTERVAL_MS = 500;
  const POLL_TIMEOUT_MS = 10000;
  let elapsed = 0;

  function pollForResults() {
    chrome.runtime.sendMessage({ action: 'getResults' }, (response) => {
      if (response) {
        renderResults(response);
      } else if (elapsed >= POLL_TIMEOUT_MS) {
        renderResults(null);
      } else {
        elapsed += POLL_INTERVAL_MS;
        setTimeout(pollForResults, POLL_INTERVAL_MS);
      }
    });
  }

  // Initial attempt
  pollForResults();

  // Event listeners for user actions
  document.getElementById('send-to-bot-btn').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.runtime.sendMessage({
        action: 'sendToBot',
        data: {
          url: tabs[0].url,
          title: tabs[0].title
        }
      });
      alert('Article sent to bot!');
    });
  });

  document.getElementById('feedback-btn-helpful').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.runtime.sendMessage({
        action: 'logFeedback',
        data: {
          analysis_id: window.__analysis_id,
          helpful: true
        }
      }, (res) => {
        alert(res?.ok ? 'Feedback logged!' : 'Feedback failed');
      });
    });
  });

  document.getElementById('feedback-btn-not-helpful').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.runtime.sendMessage({
        action: 'logFeedback',
        data: {
          analysis_id: window.__analysis_id,
          helpful: false
        }
      }, (res) => {
        alert(res?.ok ? 'Feedback logged!' : 'Feedback failed');
      });
    });
  });
});