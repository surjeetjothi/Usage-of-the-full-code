# 🚀 Render Deployment Guide for ClassBridge Backend

## ✅ Step 1: GitHub Repository Ready

Your backend code is now on GitHub:
**Repository:** https://github.com/surjeetjothi/nexuxbackend

## 📋 Step 2: Deploy on Render

### Option A: Deploy with Blueprint (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "Blueprint"

2. **Connect Repository**
   - Select "Connect a repository"
   - Choose: `surjeetjothi/nexuxbackend`
   - Click "Connect"

3. **Render will auto-detect `render.yaml`**
   - Service name: `classbridge-backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn backend:app --host 0.0.0.0 --port $PORT`

4. **Click "Apply"**

### Option B: Manual Web Service Creation

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Click "Connect a repository"
   - Select: `surjeetjothi/nexuxbackend`
   - Click "Connect"

3. **Configure Service**
   ```
   Name: classbridge-backend
   Region: Choose closest to you (e.g., Oregon, Frankfurt)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn backend:app --host 0.0.0.0 --port $PORT
   Instance Type: Free (or Starter for always-on)
   ```

4. **Click "Create Web Service"**

## 🔧 Step 3: Set Environment Variables

**CRITICAL:** You must set these before the service will work!

1. **Go to your service dashboard**
   - Click on your service name
   - Go to "Environment" tab
   - Click "Add Environment Variable"

2. **Add Required Variables:**

### Required (Must Set)

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `DATABASE_URL` | `postgresql://...` | Create PostgreSQL database on Render (see below) |
| `GROQ_API_KEY` | `gsk_xxxxx` | https://console.groq.com/keys |

### Optional (Recommended)

| Variable | Value | Purpose |
|----------|-------|---------|
| `GOOGLE_CLIENT_ID` | `xxx.apps.googleusercontent.com` | Google OAuth login |
| `SMTP_EMAIL` | `your-email@gmail.com` | Email notifications |
| `SMTP_PASSWORD` | `app-password` | Gmail app password |

3. **Click "Save Changes"**
   - Render will automatically redeploy with new variables

## 🗄️ Step 4: Create PostgreSQL Database

1. **In Render Dashboard**
   - Click "New +" → "PostgreSQL"

2. **Configure Database**
   ```
   Name: classbridge-db
   Database: classbridge
   User: classbridge_user
   Region: Same as your web service!
   PostgreSQL Version: 16
   Instance Type: Free (or paid for production)
   ```

3. **Click "Create Database"**

4. **Copy Connection String**
   - After creation, go to database dashboard
   - Find "Internal Database URL" or "External Database URL"
   - Copy the full connection string (starts with `postgresql://`)

5. **Add to Web Service**
   - Go back to your web service
   - Environment tab
   - Add/Update `DATABASE_URL` with the connection string
   - Save changes

## ⏱️ Step 5: Wait for Deployment

- **First deployment:** 3-5 minutes
- **Watch progress:** Logs tab in your service dashboard
- **Success indicator:** Logs show "Application startup complete"

## ✅ Step 6: Verify Deployment

### Test 1: Health Check
```bash
curl https://classbridge-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "ClassBridge Backend is running",
  "environment": "production",
  "database": "connected",
  "cors_enabled": true,
  "ai_enabled": true
}
```

### Test 2: Check Service URL

Your backend URL will be:
```
https://classbridge-backend.onrender.com
```

Or if you chose a different name:
```
https://YOUR-SERVICE-NAME.onrender.com
```

### Test 3: Update Frontend

If your backend URL changed, update the frontend:

**File:** `frontend/static_app/script.js` or `script.ts`

Find:
```javascript
const PROD_API_DEFAULT = 'https://classbridge-backend-bqj3.onrender.com/api';
```

Update to:
```javascript
const PROD_API_DEFAULT = 'https://classbridge-backend.onrender.com/api';
```

Then redeploy frontend on Vercel.

## 🎯 Step 7: Test Connection

### From Command Line
```bash
# Test health
curl https://classbridge-backend.onrender.com/api/health

# Test CORS
curl -H "Origin: https://ed-tech-portal.vercel.app" \
     -I https://classbridge-backend.onrender.com/api/health
```

### From Browser
1. Open: https://ed-tech-portal.vercel.app
2. Press F12 (Developer Tools)
3. Try to log in
4. Check Console for errors
5. Check Network tab for API calls

## 🔍 Troubleshooting

### Issue: Build Failed

**Check:**
- Logs tab for specific error
- `requirements.txt` is present
- Python version compatibility

**Solution:**
```bash
# Locally test build
pip install -r requirements.txt
```

### Issue: Service Crashes on Startup

**Check:**
- Logs tab for error message
- DATABASE_URL is set correctly
- Database is accessible

**Common Errors:**
- `Connection refused` → Database not accessible
- `Module not found` → Missing dependency in requirements.txt
- `Port already in use` → Restart service

### Issue: Database Connection Failed

**Check:**
- DATABASE_URL format is correct
- Database and web service in same region
- Database is running (not paused)

**Solution:**
1. Go to database dashboard
2. Check status is "Available"
3. Copy connection string again
4. Update DATABASE_URL in web service
5. Redeploy

### Issue: Free Tier Service Sleeping

**Symptom:** First request takes 30-60 seconds

**Cause:** Free tier services sleep after 15 minutes of inactivity

**Solutions:**
- Upgrade to Starter plan ($7/month) for always-on
- Accept the cold start delay
- Use a service like UptimeRobot to ping every 14 minutes

## 📊 Monitoring

### Check Service Health
- **Dashboard:** https://dashboard.render.com
- **Logs:** Service → Logs tab
- **Metrics:** Service → Metrics tab
- **Health Endpoint:** https://classbridge-backend.onrender.com/api/health

### Set Up Alerts
1. Go to service dashboard
2. Click "Settings"
3. Scroll to "Notifications"
4. Add email for deploy notifications

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
# Make changes to backend
cd "/Users/surjeet/Documents/devas change/Classbridge/class/backend_py"

# Commit and push
git add .
git commit -m "Your changes"
git push origin main

# Render automatically detects and deploys!
```

## 💰 Pricing

### Free Tier
- ✅ Good for development/testing
- ⚠️ Services sleep after 15 minutes
- ⚠️ 750 hours/month limit
- ⚠️ Slower build times

### Starter Plan ($7/month)
- ✅ Always-on (no sleeping)
- ✅ Faster builds
- ✅ Better performance
- ✅ Recommended for production

## 🎉 Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render service created and deployed
- [ ] PostgreSQL database created
- [ ] DATABASE_URL environment variable set
- [ ] GROQ_API_KEY environment variable set
- [ ] Service shows "Live" status
- [ ] Health endpoint returns "healthy"
- [ ] Frontend can connect without CORS errors
- [ ] Login functionality works
- [ ] Database operations work

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Render Status:** https://status.render.com
- **Render Community:** https://community.render.com
- **Your Service:** https://dashboard.render.com

## 🔗 Important URLs

- **GitHub Repo:** https://github.com/surjeetjothi/nexuxbackend
- **Render Dashboard:** https://dashboard.render.com
- **Backend URL:** https://classbridge-backend.onrender.com
- **Frontend URL:** https://ed-tech-portal.vercel.app
- **Health Check:** https://classbridge-backend.onrender.com/api/health
- **API Docs:** https://classbridge-backend.onrender.com/docs

---

**Last Updated:** 2026-02-07  
**Status:** Ready to Deploy  
**Next Step:** Go to https://dashboard.render.com and create your service!
