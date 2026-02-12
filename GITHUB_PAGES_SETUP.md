# GitHub Pages Auto-Deploy Setup

This repo includes a GitHub Action that automatically generates and publishes your network visualization to GitHub Pages.

## What It Does

The action:
1. ✅ Syncs latest data from your Google Sheet
2. ✅ Generates the network visualization
3. ✅ Publishes to GitHub Pages at: `https://YOUR-USERNAME.github.io/PEDP-Network-Map/`

## Triggers

The visualization updates automatically:
- **On push** to main branch
- **Daily** at 6 AM UTC
- **Manually** via GitHub Actions tab (workflow_dispatch)

## Setup (One-Time)

### 1. Ensure Google Sheet is Public

Your Google Sheet must be publicly readable:
- Open: https://docs.google.com/spreadsheets/d/1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc/
- Click **Share** → "Anyone with the link" → "Viewer"

### 2. Enable GitHub Pages

In your GitHub repo:
1. Go to **Settings** → **Pages** (left sidebar)
2. Under "Source", select: **GitHub Actions**
3. Click **Save**

### 3. Push the Workflow File

```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Pages auto-deploy workflow"
git push origin main
```

### 4. First Run

After pushing, the action will run automatically. You can also:
1. Go to **Actions** tab in GitHub
2. Click "Generate and Deploy Network Map"
3. Click **Run workflow** → **Run workflow**

## Viewing Your Site

After the first successful run:
- Your site will be at: `https://YOUR-USERNAME.github.io/PEDP-Network-Map/`
- Find the exact URL in: **Settings** → **Pages**

## How It Works

```
Google Sheets → GitHub Action → Generate Viz → GitHub Pages
    (data)         (daily)         (HTML)        (public site)
```

**Timeline:**
1. You update Google Sheet
2. Within 24 hours (or on next push), action runs
3. New visualization published automatically
4. Anyone can view the latest network map

## Manual Updates

To update immediately:
1. Go to **Actions** tab
2. Select "Generate and Deploy Network Map"
3. Click **Run workflow**

Or just push to main:
```bash
git commit --allow-empty -m "Trigger rebuild"
git push
```

## Monitoring

Check action status:
- **Actions** tab shows all runs
- Green checkmark = success
- Red X = failed (check logs)

## Troubleshooting

**Action fails at "Sync from Google Sheets"?**
- Check that Google Sheet is public
- Verify sheet IDs in `scripts/sync_from_sheets.py`
- Check action logs for details

**Action succeeds but no site?**
- Verify GitHub Pages is enabled (Settings → Pages)
- Check that source is set to "GitHub Actions"
- First deploy can take 5-10 minutes

**Want to disable auto-updates?**
- Delete `.github/workflows/deploy.yml`
- Or comment out the `schedule` section in the workflow

## Benefits

✅ **Always up-to-date** - Syncs from Google Sheet daily
✅ **No manual work** - Fully automated
✅ **Publicly shareable** - Anyone can view the network
✅ **Version controlled** - All changes tracked in git
✅ **Free hosting** - GitHub Pages is free for public repos

## Cost

**$0** - All free:
- GitHub Actions: 2,000 minutes/month free
- GitHub Pages: Free for public repos
- This workflow uses ~2 minutes per run
