# MIL Extension

Welcome to the team! This document will guide you through the process of setting up and running our Chrome extension for development.

## Getting Started

Follow these steps to load the extension into your Chrome browser.

### Prerequisites

- Google Chrome or another Chromium-based browser (like Microsoft Edge or Brave)
- Python 3.8 or higher
- FastAPI and Uvicorn (`pip install "fastapi[all]" uvicorn`)
- A local tunneling tool like localtunnel (`npm install -g localtunnel`)

### Setup and Installation

This extension is loaded as a local, "unpacked" extension. This allows you to work on the code and see your changes in real-time.

1. **Open the Extensions Page**: In your browser, type `chrome://extensions` into the address bar and press Enter.

2. **Enable Developer Mode**: In the top-right corner of the extensions page, toggle the Developer mode switch to the "on" position. This will expose new options.

3. **Load the Extension**: Click the "Load unpacked" button that appears.

4. **Select the Project Folder**: A file dialog will open. Navigate to the folder that contains this project's code and select it. Make sure you select the top-level folder, not the `manifest.json` file inside it.

Once you select the folder, the extension should appear as a new card on the extensions page and its icon will be visible in your browser's toolbar.

## Backend Setup

The extension communicates with a local backend server built with FastAPI. You will need to start this server and expose it to the public internet using a local tunneling tool.

### Start the FastAPI Server

1. Open your terminal or command prompt
2. Navigate to the directory containing your FastAPI application's main file (e.g., `main.py`)
3. Run the server using Uvicorn with the following command:

   ```bash
   uvicorn main:app --reload
   ```

4. The server will typically run on `http://127.0.0.1:8000` by default

### Start the Local Tunnel

1. In a new terminal window, start the local tunnel
2. You need to use the `--subdomain` flag to get a specific URL. Run the command, replacing `milbot` with the desired subdomain and `8000` with your FastAPI server's port:

   ```bash
   lt --port 8000 --subdomain milbot
   ```

3. The tunnel will provide a public URL like `https://milbot.loca.lt`

### Update the Extension's Code

1. You must update the extension's code to point to the new tunnel URL
2. Open the file responsible for API calls (e.g., `config.js` or `background.js`)
3. Change the hardcoded URL to your new public URL (`https://milbot.loca.lt`)

## 🐛 Troubleshooting

If the extension isn't working as expected, try these common fixes:

- **Refresh the extension**: If you've made code changes, go back to `chrome://extensions` and click the refresh button (the circular arrow icon) on the extension's card
- **Check the folder path**: Ensure the project folder has not been moved or renamed
- **Re-load**: If all else fails, remove the extension from the `chrome://extensions` page and repeat the "Setup and Installation" steps
