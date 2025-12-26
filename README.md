# FastAPI Website Category API

This project provides a blazing-fast API to fetch the category of a website domain using [categorify.org](https://categorify.org). It uses FastAPI and a local JSON cache for instant repeated lookups.

## Features

- **GET API**: `/api/category?website=example.com`
- **Ultra-fast**: Uses a local JSON cache for instant repeated queries (0s latency if cached)
- **Automatic caching**: New lookups are stored for future requests
- **Logging**: All requests and results are logged with timestamps
- **Error handling**: Graceful error messages and HTTP status codes

## Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [requests](https://docs.python-requests.org/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

Install dependencies:
```sh
pip install fastapi uvicorn requests beautifulsoup4
```

## Usage

### Run the API locally

```sh
uvicorn api_category:app --reload
```

### Example Request

```sh
curl "http://127.0.0.1:8000/api/category?website=facebook.com"
```

#### Example Response

```json
{
  "category": "Social Network",
  "cached": true
}
```

- If `cached` is `true`, the result was served instantly from the local cache.
- If `cached` is `false`, the result was fetched from categorify.org and then cached.

### API Docs

Interactive docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Files

- `api_category.py` - Main FastAPI app and API logic
- `category_cache.json` - Local cache file (auto-created)
- `api_category.log` - Log file with timestamps and request details

## Deployment

You can deploy this API to any Python server or serverless platform that supports FastAPI (e.g., Vercel, AWS Lambda, Azure Functions, etc.).

## Notes

- The cache is stored in `category_cache.json` in the working directory.
- The API respects categorify.org's usage policy. Do not abuse the upstream service.
- For best performance, keep the cache file persistent between deployments.

## License

MIT License

---

**Made with ❤️ using FastAPI**
