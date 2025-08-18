mil-extension-bot/
│
├── extension/                # Shakiran's module
│   ├── manifest.json         # Chrome Extension Manifest V3
│   ├── contentScript.js      # Injected into pages
│   ├── background.js         # Handles API comms
│   ├── popup.html            # UI for alerts + feedback
│   ├── popup.js
│   └── styles.css
│
├── api/                      # Ann's module
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── routes/           # Endpoints
│   │   │   ├── analyze.py
│   │   │   └── feedback.py
│   │   ├── core/             # Utils (LLM, Supabase, etc.)
│   │   └── models/           # Pydantic schemas
│   ├── requirements.txt
│   └── Dockerfile            # (optional for deployment)
│
├── bot/                      # Gloria's module
│   ├── telegram_bot.py       # Telegram logic
│   ├── discord_bot.py        # Discord logic
│   ├── handlers/             # Message & command handling
│   └── requirements.txt
│
├── supabase/                 # Shared resources
│   ├── schema.sql            # DB schema for feedback, logs
│   └── migrations/
│
├── docs/                     # Project docs
│   ├── workflow.md           # How extension, API, bot connect
│   └── setup.md              # Local dev setup (ngrok, env vars)
│
├── .gitignore
├── README.md                 # High-level project overview
└── LICENSE
