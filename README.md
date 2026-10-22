# TicketsAnywhere

TicketsAnywhere is an event discovery and ticket-booking web app. This branch (`main`) holds
**one React + Vite application** that serves both:

- the **customer site** at `/`
- the **admin dashboard** at `/admin` (staff/superuser only)

The Django REST API that both parts use lives on the `backend` branch
(previously the `api` branch / `ticketsany-api` repository).

**Live:** https://ticketsany.com/

## Routes

| Path | Page | Access |
|---|---|---|
| `/` | Home (banners, categories, featured events) | public |
| `/home` | Home | public |
| `/events/:category` | Events in a category (`/events/All?q=...` = search) | public |
| `/EventPageDetails/:id` | Event details and ticket ordering | public (ordering needs sign-in) |
| `/signin`, `/signup` | Customer sign-in / registration | public |
| `/profile` | Customer profile, orders and tickets | signed-in customer |
| `/admin/login` | Admin sign-in | public |
| `/admin` | Dashboard home (tickets, events overview) | admin |
| `/admin/statuschange` | Order / payment status | admin |
| `/admin/eventupload` | Event list and upload | admin |
| `/admin/events/:id/edit` | Edit an event | admin |
| `/admin/addNewEvents` | Add a new event | admin |
| `/admin/uploadbanner` | Homepage banners | admin |
| `/admin/categories` | Categories | admin |
| `/admin/alltickets` | All tickets | admin |
| `/admin/adminProfile` | Customers, IDs and events data | admin |

Any other path shows the customer 404 page; unknown `/admin/*` paths redirect to `/admin`.

Admin pages are lazy-loaded (separate chunks), use their own layout (sidebar, no customer
navbar/footer), are marked `noindex`, and keep their session in separate `localStorage` keys
(`admin_*`) so an admin login never overwrites a customer login in the same browser.
The admin login requires a Django superuser; the API enforces permissions server-side.

## Environment variables

Copy `.env.example` to `.env.local` and adjust:

| Variable | Required | Description |
|---|---|---|
| `VITE_API_BASE_URL` | yes (production) | Django API base URL including `/api/`, e.g. `https://api.example.com/api/`. Defaults to `http://127.0.0.1:8000/api/` in `npm run dev`. |
| `VITE_API_TIMEOUT` | no | Request timeout in ms (default `10000`). |
| `VITE_RETRY_ATTEMPTS` | no | Retry count (default `3`). |

All `VITE_*` values are baked into the public JavaScript bundle, so never put secrets in them.
`.env` files are git-ignored; only `.env.example` is committed.

## Local development

Requires Node.js 20+.

```bash
npm ci
cp .env.example .env.local   # then edit VITE_API_BASE_URL
npm run dev                  # http://localhost:5173 and http://localhost:5173/admin
```

## Build and quality checks

```bash
npm run lint
npm run build      # output in dist/
npm run preview    # serve the production build locally
```

GitHub Actions runs lint and the production build on pushes and pull requests.

## Deployment (Vercel)

`vercel.json` builds with Vite (`dist/`) and rewrites every non-asset path, including
`/admin` and `/admin/*`, to `index.html` so client-side routes work on refresh. Set
`VITE_API_BASE_URL` in the Vercel project environment variables. The Django API must allow the
site's origin in its CORS settings.

## Tech stack

React 19, Vite 7, React Router 7, Tailwind CSS 4, Axios, i18next (English / Myanmar),
react-toastify.

## License

No open-source license is currently declared. All rights are reserved unless a license is added by the repository owner.
