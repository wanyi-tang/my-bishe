# Reading Journal Backend

Personal reading journal and scrapbook backend API built with Node.js, Express, and MongoDB.

## Features

- 📚 Book CRUD operations
- 🔍 Advanced filtering (by genre, theme, tags, status)
- 📝 Rich text journal content support
- 🏷️ Tag system
- ⭐ Rating system (1-5 stars)
- 📖 Reading status tracking (想读，在读，已读，弃读)

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** MongoDB with Mongoose ODM
- **Environment:** dotenv

## Project Structure

```
reading-journal-backend/
├── config/
│   └── database.js          # MongoDB connection configuration
├── controllers/
│   └── bookController.js    # Business logic for books
├── middleware/
│   └── errorHandler.js      # Global error handling
├── models/
│   └── Book.js              # Mongoose schema for books
├── routes/
│   └── bookRoutes.js        # API route definitions
├── .env.example             # Environment variables template
├── server.js                # Application entry point
└── package.json
```

## Installation

1. Clone or navigate to the project directory:
```bash
cd reading-journal-backend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file from example:
```bash
copy .env.example .env
```

4. Update `.env` with your MongoDB connection string:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/reading-journal
NODE_ENV=development
```

## Running the Server

Development mode (with nodemon):
```bash
npm run dev
```

Production mode:
```bash
npm start
```

The server will start on `http://localhost:5000`

## API Endpoints

### Books

#### Get all books
```http
GET /api/books
```

Query parameters:
- `genre` - Filter by genre (e.g., 小说，散文)
- `theme` - Filter by theme (case-insensitive partial match)
- `tags` - Filter by tags (comma-separated or array)
- `search` - Search in title and author
- `status` - Filter by reading status

#### Get single book
```http
GET /api/books/:id
```

#### Create new book
```http
POST /api/books
Content-Type: application/json

{
  "title": "Book Title",
  "author": "Author Name",
  "cover": "https://example.com/cover.jpg",
  "genre": "小说",
  "theme": "成长与自我发现",
  "tags": ["经典", "推荐"],
  "content": "<p>Journal content...</p>",
  "rating": 5,
  "status": "已读"
}
```

#### Update book
```http
PUT /api/books/:id
Content-Type: application/json

{
  "title": "Updated Title",
  "rating": 4
}
```

#### Delete book
```http
DELETE /api/books/:id
```

## Book Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| title | String | Book title (required, max 200 chars) |
| author | String | Author name (required, max 100 chars) |
| cover | String | Cover image URL |
| genre | String | Literary genre (enum with Chinese values) |
| theme | String | Literary theme/topic |
| tags | Array[String] | Custom tags |
| content | String | Rich text journal content |
| rating | Number | Rating 1-5 stars |
| readDate | Date | Date finished reading |
| status | String | Reading status (想读/在读/已读/弃读) |
| createdAt | Date | Auto-generated creation timestamp |
| updatedAt | Date | Auto-generated update timestamp |

## Example Usage

### Using curl

Get all books:
```bash
curl http://localhost:5000/api/books
```

Create a book:
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"活着\",\"author\":\"余华\",\"genre\":\"小说\",\"tags\":[\"经典\",\"感人\"]}"
```

Filter by genre:
```bash
curl "http://localhost:5000/api/books?genre=小说"
```

Search books:
```bash
curl "http://localhost:5000/api/books?search=余华"
```

## Error Handling

The API uses standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Server Error

Error responses follow this format:
```json
{
  "success": false,
  "message": "Error description",
  "errors": ["Specific error messages"]
}
```

## License

MIT
