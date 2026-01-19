# Email Notifications Setup Guide

## Overview
The CI workflow is configured to send email notifications **only when workflows fail**. This ensures you're notified of issues without being overwhelmed by success notifications.

## Schedule
- **Time**: Daily at 2:00 AM SAST (00:00 UTC)
- **Frequency**: Once per day
- **Trigger**: Automatic via GitHub Actions schedule

## Email Configuration

### Required GitHub Secrets
You need to add the following secrets to your repository:

1. **EMAIL_USERNAME**: Your email address (e.g., `your-email@gmail.com`)
2. **EMAIL_PASSWORD**: Your email app password (NOT your regular password)
3. **EMAIL_TO**: Recipient email address (can be same as EMAIL_USERNAME)

### Setting Up Secrets

#### For Gmail:
1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each:
   - **Name**: `EMAIL_USERNAME`
   - **Value**: Your Gmail address (e.g., `yourname@gmail.com`)
   
   - **Name**: `EMAIL_PASSWORD`
   - **Value**: Gmail App Password (see instructions below)
   
   - **Name**: `EMAIL_TO`
   - **Value**: Email address to receive notifications (e.g., `yourname@gmail.com`)

#### Getting Gmail App Password:
1. Go to your Google Account settings
2. Navigate to **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. Select **Mail** and **Other (Custom name)**
5. Enter "GitHub Actions" as the name
6. Click **Generate**
7. Copy the 16-character password and use it as `EMAIL_PASSWORD`

### For Other Email Providers

If using a different email provider (not Gmail), update the workflow file:

```yaml
server_address: smtp.yourprovider.com
server_port: 465  # or 587 for TLS
```

Common SMTP settings:
- **Gmail**: smtp.gmail.com:465
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587

## Testing

To test email notifications:
1. Manually trigger a workflow failure
2. Or wait for the next scheduled run
3. Check your email inbox for failure notifications

## Notification Content

When a workflow fails, you'll receive an email with:
- Repository name
- Workflow name
- Run ID and commit SHA
- Direct link to the failed workflow run
- Author information

## Troubleshooting

If emails aren't being sent:
1. Verify all secrets are set correctly
2. Check that `EMAIL_PASSWORD` is an App Password (not regular password)
3. Ensure 2FA is enabled for Gmail accounts
4. Check workflow logs for email sending errors
5. Verify SMTP settings match your email provider

## Disabling Notifications

To disable email notifications, remove or comment out the `notify-on-failure` job in the workflow file.


