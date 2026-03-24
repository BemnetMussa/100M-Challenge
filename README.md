# 100M Challenge

> **Status: Active Development** — This project is a work in progress. Features are being actively built and iterated on. Expect rough edges, missing pieces, and breaking changes.

A full-stack database performance experiment: bulk-load **20 million rows** into PostgreSQL using `COPY`, then query and visualize the results through a FastAPI backend and a SvelteKit dashboard.

The goal is to push PostgreSQL to its limits, measure real query performance on large datasets, and build a clean analytics UI to display the results.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![SvelteKit](https://img.shields.io/badge/SvelteKit-2-FF3E00)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4-38BDF8)

---

## What This Does

1. **Generates** 20M synthetic event rows (page views, signups, checkouts, cart additions) using Faker
2. **Bulk-loads** them into PostgreSQL via `COPY FROM STDIN` for maximum throughput
3. **Serves** analytics through a FastAPI REST API — top events by frequency, query timing in ms
4. **Visualizes** everything in a SvelteKit dashboard with bar charts, comparison metrics, and run-over-run tracking

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│                  │     │                  │     │                  │
│   SvelteKit UI   │────▶│   FastAPI API     │────▶│   PostgreSQL 16  │
│   (Port 5173)    │     │   (Port 8000)    │     │   (Port 5432)    │
│                  │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                          ▲
                                                          │
                                                  ┌───────┴────────┐
                                                  │ generate_data  │
                                                  │ (bulk COPY)    │
                                                  └────────────────┘
```

## Tech Stack

| Layer | Tech |
|-------|------|
| **Database** | PostgreSQL 16 (Alpine) |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy, psycopg2 |
| **Data Gen** | Faker, psycopg2 `COPY FROM STDIN` |
| **Frontend** | SvelteKit 2, Svelte 5, TypeScript, Tailwind CSS v4 |
| **Charts** | Custom SVG bar chart component |
| **Icons** | lucide-svelte |
| **Containers** | Docker, Docker Compose |
| **Deployment** | Vercel adapter (frontend) |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Node.js](https://nodejs.org/) 18+ and Yarn (for the frontend)
- Python 3.11+ (if running data generation outside Docker)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/100M-Challenge.git
cd 100M-Challenge
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` if you want to change the default database credentials.

### 3. Start the backend

```bash
docker compose up -d
```

This starts PostgreSQL and the FastAPI server. The API will be available at `http://localhost:8000`.

### 4. Generate data

With the database running, generate the 20M rows:

```bash
# From your host (connects to localhost:5432)
pip install -r requirements.txt
python generate_data.py
```

Or adjust `ROWS_TO_GENERATE` via environment variable if you want a smaller test run:

```bash
ROWS_TO_GENERATE=100000 python generate_data.py
```

### 5. Start the frontend

```bash
cd client
yarn install
yarn dev
```

Open `http://localhost:5173` and click **Fetch Data**.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/users/{user_id}/events` | All events for a specific user |
| `GET` | `/analytics/events/summary` | Top 5 events by count + query time |
| `GET` | `/dashboard/data` | Full dashboard payload with performance metrics |

## Project Structure

```
100M-Challenge/
├── main.py              # FastAPI application and routes
├── database.py          # SQLAlchemy engine and session config
├── models.py            # Event ORM model
├── generate_data.py     # Bulk data generation script
├── requirements.txt     # Python dependencies
├── Dockerfile           # API container image
├── docker-compose.yml   # PostgreSQL + API orchestration
├── .env.example         # Environment variable template
└── client/              # SvelteKit frontend
    ├── src/
    │   ├── routes/
    │   │   └── +page.svelte        # Main dashboard page
    │   └── lib/components/
    │       ├── AnalyticsChart.svelte      # Bar chart visualization
    │       ├── ComparisonMetrics.svelte   # Run-over-run comparison cards
    │       └── DashboardPanel.svelte      # Reusable metric panel
    ├── package.json
    └── svelte.config.js
```

## Roadmap

This project is still being actively developed. Here's what's planned:

- [ ] System status panel (dataset size, load time, DB health)
- [ ] Performance comparison dashboard (before/after optimization)
- [ ] Query optimization experiments (indexes, partitioning, materialized views)
- [ ] Pagination for user events endpoint
- [ ] Server-side rendering for dashboard data
- [ ] Benchmarking suite with reproducible results
- [ ] Support for 100M+ rows

## Contributing

This project is in early development, but contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/something`)
3. Commit your changes (`git commit -m 'Add something'`)
4. Push to the branch (`git push origin feature/something`)
5. Open a Pull Request

## License

MIT
