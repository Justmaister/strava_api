# Strava API Setup Guide

This guide will walk you through the process of setting up your Strava API credentials and obtaining the necessary tokens for the application.

## 1. Create a Strava APP and get Credentials

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application
3. Set the following:
   - Authorization Callback Domain: `developers.strava.com`
   - Website: `https://www.strava.testapp.com`

## 2. Authorize Credentials in the Browser

Visit the following URL, replacing `[REPLACE_WITH_YOUR_CLIENT_ID]` with your actual client ID from the Strava API settings:
```
http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
```

> **Note**: The `scope=activity:read_all` parameter sets the permissions for your app. For more information about API permissions, visit the [Strava Developers Playground](https://developers.strava.com/playground/).

## 3. Get Strava Access Code

After authorization, you'll be redirected to a URL like:

```
http://localhost/exchange_token?state=&code=[code]&scope=read,activity:read_all
```

Copy the `code` value from this URL.

## 4. Get Strava Access and Refresh Tokens

Make a POST request to `https://www.strava.com/oauth/token` with the following parameters:

- `client_id`: Your Strava client ID
- `client_secret`: Your Strava client secret
- `code`: The code from step 3
- `grant_type`: `authorization_code`

Example URL:

```
https://www.strava.com/oauth/token?client_id=xxxxxxx&client_secret=xxxxxxxxxxxxxxxxxxxxxx&code=1c49xxxxxxxxxxxxxxxxxxxxxxx&grant_type=authorization_code
```

The response will include:
- `access_token`: Used for API requests
- `refresh_token`: Used to get new access tokens
- `expires_at`: Unix timestamp when the access token expires

## Important Notes

- Access tokens expire at the `expires_at` time
- Store your tokens securely
- Never commit tokens to version control
- Use the refresh token to obtain new access tokens when they expire

## Additional Resources

- [Strava Developer Playground](https://developers.strava.com/playground/)
- [Strava API Documentation](https://developers.strava.com/docs/)
- [Srava aPI Reference](https://developers.strava.com/docs/)