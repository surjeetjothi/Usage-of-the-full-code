# Implementation Plan: Unified Deployment on Render

## Objective
Deploy both the Frontend (Static Site) and Backend (FastAPI) of the **ClassBridge/Noble Nexus** application to a single platform (**Render**) using a Blueprint configuration.

## Current Status
- **Blueprint Created**: A `render.yaml` file has been created in the root directory. This file defines both services so Render can deploy them simultaneously.
- **CORS Updated**: The Backend (`backend/backend.py`) has been updated to accept requests from any Render subdomain (`.onrender.com`), ensuring the new frontend can communicate with it.

## Step-by-Step Implementation Guide

### Phase 1: Preparation (Completed by Assistant)
1.  **Root Configuration**: Created `render.yaml` in the root folder.
2.  **Backend Tuning**: Modified `backend.py` to allow CORS origins from `onrender.com`.

### Phase 2: User Actions (Required)

#### Step 1: Push Changes to GitHub
You need to push the new `render.yaml` and updated `backend/backend.py` to your GitHub repository.
```bash
git add .
git commit -m "feat: Add Render blueprint and update CORS for unified deployment"
git push
```

#### Step 2: Create Blueprint Instance on Render
1.  Log in to your [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository.
4.  Render will auto-detect the `render.yaml` file.
5.  **Service Names**: You will see `classbridge-backend` and `classbridge-frontend`.
6.  Click **Apply** or **Create Blueprint**.

#### Step 3: Configure Environment Variables
The blueprint creates the services but does **not** fill in sensitive secrets. You must add them manually in the Render Dashboard.
1.  Go to the **Dashboard** -> **classbridge-backend**.
2.  Click **Environment**.
3.  Add the following variables (copy values from your local `.env` or previous deployment):
    - `DATABASE_URL`: (Your PostgreSQL connection string)
    - `GROQ_API_KEY`: (Your AI API Key)
    - `SMTP_EMAIL`: (Optional: for emails)
    - `SMTP_PASSWORD`: (Optional: for emails)
    - `GOOGLE_CLIENT_ID`: (Optional: for OAuth)

#### Step 4: Update Frontend Connection
Once the backend is deployed, Render will assign it a unique URL (e.g., `https://classbridge-backend-xyz.onrender.com`).
1.  Copy this **new Backend URL**.
2.  Open `frontend/script.ts` (or `.js`) in your local editor.
3.  Update the `API_BASE_URL` logic:
    ```typescript
    // Replace the old URL with the new one from Step 4
    : 'https://classbridge-backend-new-url.onrender.com/api';
    ```
4.  Commit and push this change:
    ```bash
    git add frontend/script.ts
    git commit -m "fix: Point frontend to new Render backend URL"
    git push
    ```
5.  Render will automatically redeploy the Frontend with the correct connection.

## Verification
- Visit the **Frontend URL** provided by Render.
- Try logging in.
- Verify that data is loading from the backend (e.g., check the network tab for successful requests to `/api/...`).

## Troubleshooting
- **Build Failures**: Check the "Logs" tab in Render for specific error messages.
- **CORS Errors**: Ensure the `backend.py` change was successfully pushed and deployed.
- **Database Connection**: Verify `DATABASE_URL` is correct in the Render Environment settings.
