# Frontend-Backend Connection Fix Guide

## Problem Summary
Your frontend (deployed on Vercel at https://ed-tech-portal.vercel.app) is not connecting to your backend (deployed on Render at https://classbridge-backend-bqj3.onrender.com).

## Changes Made

### 1. Backend CORS Configuration (backend.py)
✅ **Updated CORS to support all Vercel deployments**
- Added regex pattern to allow all `*.vercel.app` domains in production
- This handles preview deployments and the main domain
- Separated production and development CORS policies

### 2. Health Check Endpoint
✅ **Added `/api/health` endpoint**
- Test if backend is running: `https://classbridge-backend-bqj3.onrender.com/api/health`
- Returns server status, database connection, and configuration info

## Required Actions

### Step 1: Verify Backend is Running on Render

1. **Visit your Render dashboard**: https://dashboard.render.com
2. **Check your service status**: Look for "noble-nexus-backend" or similar
3. **Verify it's deployed and running** (should show green/active status)

### Step 2: Set Environment Variables on Render

Your backend needs these environment variables set in Render:

**Required Variables:**
```
DATABASE_URL=<your-postgres-connection-string>
GROQ_API_KEY=<your-groq-api-key>
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
SMTP_EMAIL=<your-email-for-notifications>
SMTP_PASSWORD=<your-email-app-password>
```

**To set these:**
1. Go to your Render service dashboard
2. Click on "Environment" tab
3. Add each variable with its value
4. Click "Save Changes"
5. Render will automatically redeploy

### Step 3: Update Render.yaml (if needed)

The current `render.yaml` configuration looks good, but verify:
- Build command: `pip install -r backend_py/requirements.txt`
- Start command: `cd backend_py && uvicorn backend:app --host 0.0.0.0 --port $PORT`

### Step 4: Deploy Updated Backend

**Option A: Push to GitHub (Recommended)**
```bash
cd "/Users/surjeet/Documents/devas change/Classbridge/class/backend_py"
git add backend.py
git commit -m "Fix CORS for Vercel deployment and add health check"
git push origin main
```

**Option B: Manual Deployment on Render**
1. Go to your Render service
2. Click "Manual Deploy" → "Deploy latest commit"

### Step 5: Test the Connection

1. **Test health endpoint:**
   ```
   https://classbridge-backend-bqj3.onrender.com/api/health
   ```
   Should return JSON with status "healthy"

2. **Test from frontend:**
   - Open https://ed-tech-portal.vercel.app
   - Open browser console (F12)
   - Look for API requests to `classbridge-backend-bqj3.onrender.com`
   - Check for CORS errors (should be gone now)

3. **Test login:**
   - Try logging in with a test account
   - Check network tab for successful API calls

## Common Issues & Solutions

### Issue 1: "Failed to fetch" or "Network Error"
**Cause:** Backend not running or wrong URL
**Solution:** 
- Verify backend is deployed and running on Render
- Check the URL is exactly: `https://classbridge-backend-bqj3.onrender.com`

### Issue 2: CORS Error
**Cause:** CORS not configured for your domain
**Solution:**
- The fix we applied should resolve this
- Redeploy backend after pushing changes

### Issue 3: 502 Bad Gateway
**Cause:** Backend crashed or database connection failed
**Solution:**
- Check Render logs for errors
- Verify DATABASE_URL environment variable is set correctly
- Check if database is accessible from Render

### Issue 4: Render Service Sleeping
**Cause:** Free tier services sleep after inactivity
**Solution:**
- Upgrade to paid plan for always-on service
- Or accept 30-second cold start on first request

## Verification Checklist

- [ ] Backend deployed and running on Render
- [ ] Environment variables set on Render
- [ ] Health check endpoint returns "healthy"
- [ ] Frontend can make API calls without CORS errors
- [ ] Login functionality works
- [ ] Database operations work

## Network Configuration

### Render IP Addresses
You mentioned these IPs:
- 74.220.52.0/24
- 74.220.60.0/24

**Note:** You don't need to configure these IPs anywhere. Render handles networking automatically. These are just the outbound IP ranges Render uses.

### Vercel Configuration
Your `vercel.json` is configured correctly for SPA routing. No changes needed there.

## Testing Commands

```bash
# Test backend health
curl https://classbridge-backend-bqj3.onrender.com/api/health

# Test CORS from command line
curl -H "Origin: https://ed-tech-portal.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://classbridge-backend-bqj3.onrender.com/api/auth/login

# Should return CORS headers in response
```

## Next Steps

1. **Deploy the backend changes** (push to GitHub or manual deploy on Render)
2. **Wait for deployment** (usually 2-5 minutes)
3. **Test health endpoint** to confirm backend is running
4. **Test frontend** to verify connection works
5. **Check browser console** for any remaining errors

## Support

If issues persist after following this guide:
1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify all environment variables are set correctly
4. Ensure database is accessible from Render
