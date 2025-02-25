# RedTeamGO Frontend

A modern React frontend for the RedTeamGO application, providing a user-friendly interface for LLM red teaming and analysis.

## Features

- Modern, responsive UI using Chakra UI
- Real-time form validation
- Interactive data visualization
- Dark/Light mode support
- Type-safe development with TypeScript

## Getting Started

### Prerequisites

- Node.js 18 or later
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

3. Start the development server:
```bash
npm start
```

The application will be available at http://localhost:3001

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Project Structure

```
src/
├── api/          # API client and types
├── components/   # Reusable UI components
├── pages/        # Page components
├── theme/        # Chakra UI theme customization
└── utils/        # Utility functions
```

## Docker Support

The frontend is containerized and can be run using Docker:

```bash
# Build the image
docker build -t redteamgo-frontend .

# Run the container
docker run -p 3001:3001 redteamgo-frontend
```

Or using docker-compose:

```bash
docker-compose up
```

## Features

### Dashboard
- System health monitoring
- Quick access to all features
- Real-time status updates

### Toxicity Analysis
- Batch analysis of prompts
- Real-time toxicity checking
- Customizable sampling options

### Bias Detection
- Multiple bias categories
- Customizable prompt libraries
- Detailed analysis results

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request