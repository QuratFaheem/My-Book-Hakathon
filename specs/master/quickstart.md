# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js v18.x or higher
- npm or yarn package manager
- Python 3.11 or higher
- Git for version control

## Getting Started

### 1. Clone the Repository

```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Set up Backend Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_url_here
DATABASE_URL=your_database_url_here
SECRET_KEY=your_secret_key_here
```

### 5. Initialize the RAG Backend

```bash
# From the backend directory
python -m src.initialize_db
```

### 6. Run the Development Server

**Frontend (Docusaurus):**

```bash
# From the project root
npm start
```
This command starts the Docusaurus development server and opens the textbook in your browser at `http://localhost:3000`.

**Backend (FastAPI):**

```bash
# From the backend directory
uvicorn main:app --reload
```
This command starts the backend server at `http://localhost:8000`.

## Project Structure

```
physical-ai-textbook/
├── docs/                 # Textbook content
│   ├── intro/
│   ├── physical-ai/
│   ├── ros2/
│   ├── ...
├── src/                  # Frontend custom components
│   ├── components/
│   ├── pages/
│   └── css/
├── backend/              # RAG chatbot backend
│   ├── src/
│   ├── routers/
│   └── tests/
├── static/               # Static assets
├── package.json          # Frontend dependencies
├── docusaurus.config.js  # Docusaurus configuration
├── sidebars.js          # Navigation structure
└── README.md            # Project overview
```

## Adding New Content

### Adding a New Chapter

1. Create a new directory in the `docs/` folder:
   ```bash
   mkdir docs/new-chapter-name
   ```

2. Create the main markdown file:
   ```bash
   touch docs/new-chapter-name/index.md
   ```

3. Add the following frontmatter to your markdown file:
   ```md
   ---
   sidebar_position: X  # Replace X with the desired position
   ---

   # Chapter Title

   Your chapter content here...
   ```

4. Update `sidebars.js` to include the new chapter:
   ```js
   module.exports = {
     tutorialSidebar: [
       // ... existing items
       {
         type: 'category',
         label: 'New Chapter Name',
         items: ['new-chapter-name/index'],
       },
     ],
   };
   ```

### Adding Code Examples

To include executable code examples in your content:

1. Create a code block with the appropriate language tag:
   ````md
   ```python
   # Your code here
   import rospy

   def hello_world():
       print("Hello, Physical AI World!")
   ```
   ````

2. For executable examples with verification, add a comment indicating verification status:
   ```md
   <!-- VERIFIED: [date] - Runs successfully on ROS 2 Humble -->
   ```

## Working with the RAG Chatbot

### Adding Content to the Knowledge Base

1. After adding new documentation, update the vector database:
   ```bash
   # From the backend directory
   python -m src.ingest_docs
   ```

2. The script will parse all documents in the `docs/` directory and store vector embeddings in Qdrant.

### Testing the Chat Interface

1. Send a test query to the backend:
   ```bash
   curl -X POST "http://localhost:8000/api/chat" \
        -H "Content-Type: application/json" \
        -d '{
          "message": "What is Physical AI?",
          "session_id": "test-session"
        }'
   ```

## Building for Production

### Building the Frontend

```bash
npm run build
```

This command creates a static build in the `build/` directory, which can be served using any static hosting service.

### Serving the Complete Application

1. Deploy the built frontend to your static hosting provider (e.g., GitHub Pages)
2. Deploy the backend service to a server that supports Python applications
3. Update the frontend to point to your deployed backend API endpoint in `docusaurus.config.js`

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Check if another process is using the default port (3000 for frontend, 8000 for backend)
   - Kill the process or use a different port with `npm start --port [number]` or `uvicorn main:app --port [number]`

2. **API key errors**
   - Verify your environment variables are properly set
   - Check that the `.env` file is in the correct directory (backend/)
   - Restart the backend server after updating environment variables

3. **Docusaurus build errors**
   - Run `npm run clear` to clear the cache
   - Verify all markdown files have correct syntax
   - Check that all referenced images and links exist