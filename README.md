# Vietnam Stock Analyzer

A comprehensive multi-agent AI-powered stock analysis system for Vietnam stock market, featuring real-time data visualization, intelligent chat interface, and advanced technical analysis.

## 🚀 Features

### 📊 **Real-Time Stock Analysis**
- **Live Data**: Real-time stock prices and market data
- **Technical Indicators**: RSI, MACD, Moving Averages, Volume Analysis
- **Interactive Charts**: Beautiful, responsive stock charts with Recharts
- **Multi-Agent Analysis**: AI-powered insights from multiple specialized agents

### 💬 **Intelligent Chat Interface**
- **Dynamic Analysis**: AI responds to specific user questions
- **Context-Aware**: Understands buy/sell recommendations, price analysis, technical analysis
- **Vietnamese Language**: Natural language processing for Vietnamese stock queries
- **Real-Time Responses**: Instant analysis based on current market data

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Theme**: Full theme switching with persistent preferences
- **Beautiful Layout**: Balanced, professional design with Tailwind CSS
- **Interactive Components**: Smooth animations and transitions

### 📈 **Advanced Analytics**
- **Quick Analysis**: Fast AI-powered stock recommendations
- **Market Sentiment**: News sentiment analysis and market trends
- **Risk Assessment**: Comprehensive risk evaluation and scoring
- **Prediction Models**: Short-term trend predictions with confidence levels

## 🏗️ Architecture

### **Backend (FastAPI + Python)**
- **Multi-Agent System**: Specialized AI agents for different analysis types
- **Real-Time Data**: Integration with Vietnam stock market APIs
- **Async Processing**: High-performance async request handling
- **CORS Enabled**: Secure cross-origin resource sharing

### **Frontend (Next.js + React)**
- **TypeScript**: Type-safe development experience
- **Tailwind CSS**: Modern, utility-first styling
- **Shadcn/ui**: Professional UI component library
- **Recharts**: Interactive data visualization

### **Key Technologies**
- **Backend**: FastAPI, Python, asyncio, Pydantic
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Charts**: Recharts library for beautiful visualizations
- **UI Components**: Shadcn/ui with Lucide icons

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- npm or yarn

### **Backend Setup**

1. Navigate to the project directory:
```bash
cd Stock_Analyzer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000`

### **Frontend Setup**

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## 📊 API Endpoints

### **Stock Data**
- `GET /api/v1/stocks` - Get list of Vietnam stocks
- `POST /api/v1/quick-analyze` - Get quick AI analysis for a stock
- `GET /api/v1/stock/{ticker}/data` - Get detailed stock data

### **Chat & Analysis**
- `POST /api/v1/chat` - AI-powered chat analysis
- `GET /api/v1/market-sentiment` - Get market sentiment analysis
- `POST /api/v2/analyze` - Full multi-agent analysis (async)

### **System**
- `GET /health` - Health check endpoint
- `GET /` - API information and endpoints

## 🎯 Usage Examples

### **Chat Analysis**
Ask questions like:
- "Có nên mua VCB không?" (Should I buy VCB?)
- "Giá FPT hôm nay thế nào?" (How is FPT's price today?)
- "RSI của VNM là bao nhiêu?" (What is VNM's RSI?)
- "Dự đoán xu hướng HPG?" (Predict HPG's trend?)

### **Stock Selection**
1. Browse the stock list on the left sidebar
2. Click on any stock to see detailed analysis
3. Switch between Dashboard and Chat tabs
4. View interactive charts and indicators

### **Theme Switching**
- Click the theme toggle button in the header
- Choose between Light, Dark, or System theme
- Preferences are automatically saved

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the `app` directory:
```env
# API Keys (if using external services)
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_news_api_key

# Database (if needed)
DATABASE_URL=your_database_url
```

### **Next.js Configuration**
The frontend uses proxy configuration to handle CORS:
```typescript
// next.config.ts
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/api/:path*',
    },
  ];
},
```

## 🎨 Features Showcase

### **📈 Interactive Charts**
- Price trends with gradient fills
- Volume analysis with bar charts
- Reference lines for average prices
- Responsive design for all screen sizes

### **💬 Smart Chat**
- Context-aware responses
- Vietnamese language support
- Real-time analysis generation
- Professional markdown formatting

### **🌓 Theme System**
- Complete dark/light mode support
- System preference detection
- Persistent user preferences
- Smooth transitions

## 🚀 Deployment

### **Backend Deployment**
```bash
# Using Docker
docker build -t vietnam-stock-analyzer .
docker run -p 8000:8000 vietnam-stock-analyzer

# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### **Frontend Deployment**
```bash
# Build for production
npm run build

# Start production server
npm start

# Or deploy to Vercel
vercel --prod
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Next.js Team** - For the amazing React framework
- **FastAPI** - For the high-performance Python web framework
- **Vietnam Stock Market** - For providing the data that powers this analysis
- **AI Community** - For the inspiration and tools that make intelligent analysis possible

## 📞 Support

For support, questions, or contributions:
- Create an issue on GitHub
- Check the API documentation at `http://localhost:8000/docs`
- Review the code comments for detailed explanations

---

**Built with ❤️ for Vietnam's stock market community**

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
