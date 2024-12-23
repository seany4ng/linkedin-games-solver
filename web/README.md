# Frontend

We use a React/Typescript frontend with vite for building the project. Before starting, make sure your npm and node versions are supported. The dependencies will generally require:
- `node -v` >= 16.18
- `npm -v` >= 8.3

If you don't have node or npm installed, get them installed with versions satisfying the above constraints. Once done, install the required dependencies:

```bash
npm install
```

Start the dev server:

```bash
npm run dev
```

And open the app locally in a browser:

```
http://localhost:5173
```

**Note: this requires starting the backend server first. See `../core` for details.**

### Frontend: Troubleshooting

Either npm sucks or I'm bad at using it, but I routinely face issues with `vite` and `node_modules`. If this is you, I've found that re-installing everything typically works.

```bash
rm -rf node_modules package-lock.json
npm install
```

Once in a while, `vite` will suddenly be not found -- I have no clue why. Whenever this happens, I use the above commands, similar to how back in the day, IT support primarily consisted of turning the machine off and on again.

Secondly, I currently hard-code the base URL to be the one used in production. Assuming you are testing locally, change the URL in `src/api/client.ts`:

```
(-) baseURL: 'https://seany4ng--linkedin-games-solver-run-app.modal.run',
(+) baseURL: 'http://localhost:8000',
```