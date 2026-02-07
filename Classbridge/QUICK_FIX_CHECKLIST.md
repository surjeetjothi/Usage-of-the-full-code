# Quick Fix Checklist for ClassBridge Deployment

## Immediate Actions Required

### 1. Deploy Backend Changes ⚡
```bash
cd "/Users/surjeet/Documents/devas change/Classbridge/class/backend_py"

# Add and commit changes
git add backend.py
git commit -m "Fix CORS for Vercel and add health check endpoint"

# Push to trigger Render deployment
git push origin main
```

### 2. Verify Render Environment Variables 🔧

Go to: https://dashboard.render.com → Your Service → Environment

**Required Variables:**
| Variable | Example Value | Status |
|----------|---------------|--------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | ❗ Required |
| `GROQ_API_KEY` | `gsk_...` | ❗ Required |
| `GOOGLE_CLIENT_ID` | `xxx.apps.googleusercontent.com` | Optional |
| `SMTP_EMAIL` | `your-email@gmail.com` | Optional |
| `SMTP_PASSWORD` | `app-password` | Optional |

### 3. Test Connection 🧪

After deployment completes (2-5 minutes):

```bash
# Test from command line
curl https://classbridge-backend-bqj3.onrender.com/api/health

# Or run the test script
python3 test_connection.py
```

### 4. Check Frontend Console 🔍

1. Open https://ed-tech-portal.vercel.app
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Look for:
   - ✅ "ClassBridge API Base URL: https://classbridge-backend-bqj3.onrender.com/api"
   - ❌ CORS errors (should be gone after fix)
   - ❌ Network errors (check backend is running)

## What We Fixed

### Backend Changes (backend.py)

1. **CORS Configuration**
   - ✅ Added regex pattern for all Vercel domains
   - ✅ Supports preview deployments
   - ✅ Separate production/development configs

2. **Health Check Endpoint**
   - ✅ New endpoint: `/api/health`
   - ✅ Returns server status and diagnostics

### Why It Wasn't Working

**Problem:** CORS was only allowing specific Vercel URLs, not all deployments

**Solution:** Use regex pattern `https://.*\.vercel\.app` in production

## Common Issues

### Issue: "Backend timeout" or "Service sleeping"
**Cause:** Free tier Render services sleep after 15 minutes of inactivity  
**Fix:** 
- Wait 30-60 seconds for service to wake up
- Or upgrade to paid plan ($7/month) for always-on service

### Issue: "CORS error" in browser console
**Cause:** Backend not deployed with new CORS config  
**Fix:** 
- Push changes to GitHub
- Wait for Render to auto-deploy
- Clear browser cache

### Issue: "Failed to fetch" or "Network error"
**Cause:** Backend not running or wrong URL  
**Fix:**
- Check Render dashboard - service should be "Active"
- Verify URL is exactly: `https://classbridge-backend-bqj3.onrender.com`
- Check Render logs for errors

### Issue: "Database connection error"
**Cause:** DATABASE_URL not set or incorrect  
**Fix:**
- Set DATABASE_URL in Render environment variables
- Format: `postgresql://user:password@host:port/database`
- Render provides this automatically if you created a PostgreSQL database

## Verification Steps

- [ ] Backend changes committed and pushed to GitHub
- [ ] Render deployment completed successfully
- [ ] Health endpoint returns "healthy" status
- [ ] Frontend loads without console errors
- [ ] Login functionality works
- [ ] No CORS errors in browser console

## Quick Test URLs

```bash
# Backend health check
https://classbridge-backend-bqj3.onrender.com/api/health

# Backend root (should show "API is Running")
https://classbridge-backend-bqj3.onrender.com/

# Frontend
https://ed-tech-portal.vercel.app/
```

## Need Help?

1. **Check Render Logs:**
   - Go to Render Dashboard → Your Service → Logs
   - Look for errors during startup or requests

2. **Check Browser Console:**
   - F12 → Console tab
   - Look for red error messages

3. **Run Test Script:**
   ```bash
   python3 test_connection.py
   ```

## Next Steps After Fix

1. Test login with a user account
2. Verify database operations work
3. Test AI features (if GROQ_API_KEY is set)
4. Check all major features work correctly

---

**Last Updated:** 2026-02-07  
**Status:** Awaiting deployment of backend changes
