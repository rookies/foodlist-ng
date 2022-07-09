foodlist-ng
===========

## Frontend
```sh
npm install
npm run dev    # Compile and Hot-Reload for Development
npm run build  # Type-Check, Compile and Minify for Production
npm run lint   # Lint with ESLint
```

## Backend
```sh
docker run -e POSTGRES_USER=foodlist -e POSTGRES_PASSWORD=foodlist -p 5432:5432 --rm -it postgres
python3 -m alembic revision --autogenerate -m "<msg>"
python3 -m uvicorn --reload foodlist.main:app
```
