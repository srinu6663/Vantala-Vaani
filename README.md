# Vantala Vaani 🍽️

A fullstack content contribution platform for food-related media, built with Vite + React (frontend) and Node.js (backend).

## Features

- User authentication (login, JWT)
- Upload text, audio, video, and images (with chunked upload for large files)
- Dashboard with user stats and recent contributions
- User profile with name and avatar
- Accessible, modern UI (Radix UI, Tailwind CSS)
- API integration with corpus.swecha.org

## Project Structure

```
CorpusUpload/
├── client/         # Frontend (Vite + React)
│   ├── src/
│   └── ...
├── server/         # Backend (Node.js, API routes)
│   └── ...
├── shared/         # Shared schemas (zod)
├── uploads/        # Uploaded files (if local)
├── package.json    # Project metadata
└── ...
```

## Getting Started (Local)

1. **Clone the repo:**
   ```sh
   git clone https://github.com/srinu6663/Vantala-Vaani.git
   cd CorpusUpload
   ```
2. **Install dependencies:**
   ```sh
   cd client && npm install
   cd ../server && npm install
   ```
3. **Run frontend:**
   ```sh
   cd client
   npm run dev
   ```
4. **Run backend:**
   ```sh
   cd server
   npm start
   ```

## Deployment (Render)

- Push your code to GitHub.
- Create two services on [Render](https://render.com/):
  - **Static Site** for `client/` (build: `npm install && npm run build`, publish: `dist`)
  - **Web Service** for `server/` (build: `npm install`, start: `npm start`)
- Set environment variables as needed (API URLs, secrets).

## Environment Variables

- `VITE_API_BASE_URL` (frontend)
- `API_BASE_URL` (backend)
- Any secrets required for authentication

## License

MIT

---

Made with ❤️ for the food community.
