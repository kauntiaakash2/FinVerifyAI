# FinVerifyAI Deployment Guide

## Prerequisites

- GitHub account with repository access
- Vercel account (free tier is sufficient)
- API Keys configured in environment variables

## Required API Keys

Set these as environment variables in Vercel Dashboard:

1. **FMP_API_KEY** - Financial Modeling Prep
   - Get from: https://financialmodelingprep.com/register

2. **ALPHA_VANTAGE_KEY** - Alpha Vantage
   - Get from: https://www.alphavantage.co/support/#api-key

3. **FRED_API_KEY** - FRED Economic Data
   - Get from: https://fred.stlouisfed.org/docs/api/api_key.html

## Deployment Steps

### 1. Via Vercel Dashboard (Recommended)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository (`kauntiaakash2/FinVerifyAI`)
4. Configure environment variables:
   - Go to Settings → Environment Variables
   - Add your API keys
5. Deploy

### 2. Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# For production deployment
vercel --prod
```

## Environment Variables

Required environment variables for Vercel:

```
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
CACHE_TTL=300
RATE_LIMIT_PER_MINUTE=10
PRIMARY_DATA_SOURCE=yfinance
FMP_API_KEY=your_api_key_here
ALPHA_VANTAGE_KEY=your_api_key_here
FRED_API_KEY=your_api_key_here
```

## Project Structure for Vercel

```
FinVerifyAI/
├── api/
│   └── index.py                 # Vercel entrypoint
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app definition
│   ├── config.py                # Configuration
│   ├── models.py                # Pydantic models
│   ├── verifier.py              # Claim verification logic
│   ├── data_fetcher.py          # Financial data fetching
│   └── utils.py                 # Utilities & logging
├── frontend/
│   ├── index.html               # Frontend UI
│   └── script.js                # Frontend logic
├── requirements-prod.txt        # Production dependencies
├── vercel.json                  # Vercel configuration
└── .vercelignore                # Files to ignore in deployment
```

## API Endpoints

After deployment, access your API at:
```
https://your-app.vercel.app/
```

### Available Endpoints:

- **GET** `/` - Home page
- **GET** `/docs` - Swagger API documentation
- **GET** `/api/health` - Health check
- **POST** `/api/verify` - Verify financial claims
- **GET** `/api/companies` - List supported companies
- **GET** `/api/examples` - Get example claims
- **GET** `/api/metrics/{ticker}` - Get company metrics
- **GET** `/api/historical/{ticker}` - Get historical prices

## Example API Request

```bash
curl -X POST https://your-app.vercel.app/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Apple revenue is $394 billion"
  }'
```

## Monitoring

### Check Deployment Status:
1. Go to Vercel Dashboard
2. Select your project
3. View deployment logs in "Deployments" tab

### View Runtime Logs:
1. Click on a deployment
2. Select "Functions" tab
3. View logs for `api/index.py`

## Troubleshooting

### Issue: 500 Internal Server Error

**Solution:** Check the logs in Vercel dashboard:
1. Go to Deployments
2. Click the failed deployment
3. View the "Functions" logs
4. Check environment variables are set correctly

### Issue: API Keys Not Working

**Solution:** Verify environment variables:
1. Go to Project Settings → Environment Variables
2. Ensure all required keys are set
3. Redeploy the project

### Issue: Rate Limit Exceeded

**Solution:** Adjust rate limiting in `vercel.json`:
```json
"RATE_LIMIT_PER_MINUTE": "50"
```

## Performance Optimization

- **Caching**: Financial data is cached for 300 seconds (configurable)
- **Async Processing**: All operations are async for better performance
- **Timeouts**: API calls have 5-second timeouts to prevent hanging

## Security Considerations

1. ✅ API keys stored securely as environment variables
2. ✅ Rate limiting enabled (10 requests/minute per IP)
3. ✅ No sensitive data in logs
4. ✅ CORS enabled for frontend access
5. ✅ Input validation on all requests

## Rollback to Previous Deployment

If something goes wrong:
1. Go to Vercel Dashboard
2. Click on project
3. Go to Deployments
4. Find the previous stable deployment
5. Click "..." and select "Promote to Production"

## Support

For issues or questions:
- Check [Vercel Documentation](https://vercel.com/docs)
- Review [FastAPI Documentation](https://fastapi.tiangolo.com/)
- Check application logs in Vercel dashboard

## Next Steps

After deployment:
1. Test all API endpoints using Swagger UI at `/docs`
2. Monitor logs for any errors
3. Adjust rate limiting if needed
4. Consider caching strategy based on usage patterns
