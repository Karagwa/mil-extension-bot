// This function attempts to find and extract the main article content in the webpage.
function extractArticleText() {
  const selectors = [
    'article',  // Common HTML5 element for articles
    'main',     // Main content area
    'div[role="main"]',  // ARIA role for main content
    '.entry-content', // WordPress specific class
    '.post-content',  // Common class for blog post content
    '#main-content',  // Common ID for main content
    '#content',      // Common ID for content
    '#article-body', // Common ID for article body
  ];

  for (const selector of selectors) {
    const element = document.querySelector(selector);
    if (element && element.innerText.length > 500) {
      return element.innerText;
    }
  }
  return document.body.innerText;
}

// This function extracts all unique links from the page.
function extractLinks() {
  const links = new Set();
  const aTags = document.querySelectorAll('a');

  // Looping through all <a> tags and add their 'href' attribute to a Set.
  // Using a Set automatically handles duplicates.
  aTags.forEach(tag => {
    const href = tag.getAttribute('href');
    if (href && href.startsWith('http')) {
      // We only want to check external web links, not internal page anchors or mailto links.
      links.add(href);
    }
  });

  return Array.from(links); // Convert the Set back to an array for easy transport.
}

// Get the article text and links from the current page.
const articleText = extractArticleText();
const articleUrl = window.location.href;
const articleTitle = document.title;
const extractedLinks = extractLinks();

// Send the complete data package to the background service worker.
// The service worker will receive this message and send the data to the API endpoints.
chrome.runtime.sendMessage({
  action: 'analyzeContent',
  data: {
    text: articleText,
    url: articleUrl,
    title: articleTitle,
    links: extractedLinks, // The list of links
  }
});

// This listener waits for a message from background.js with the analysis results.
chrome.runtime.onMessage.addListener((response) => {
  if (response.action === 'displayResults') {
    const results = response.data;
    if (results) {
      // Create a warning banner if misinformation is detected
      if (results.analysis.isMisinformation) {
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('misinformation-alert');
        alertDiv.textContent = 'This content may be false or misleading.';
        document.body.prepend(alertDiv);
      }

      // Adding a warning for AI-generated content
      if (results.analysis.isAiGenerated) {
        const warningDiv = document.createElement('div');
        warningDiv.classList.add('ai-generated-warning');
        warningDiv.textContent = 'This content is likely AI-generated.';
        document.body.prepend(warningDiv);
      }

      // Highlight potentially false links
      if (results.links && results.links.potentiallyFalse.length > 0) {
        const allLinks = document.querySelectorAll('a');
        results.links.potentiallyFalse.forEach(falseLinkUrl => {
          allLinks.forEach(link => {
            if (link.href === falseLinkUrl) {
              link.classList.add('potentially-false-link');
            }
          });
        });
      }
    }
  }
});