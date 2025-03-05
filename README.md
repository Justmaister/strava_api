# Strava API Project


# Steps

## 1- Create a Strava APP and get Credentials

Go the the link https://www.strava.com/settings/api and Create an App and set Authorization Callback Domain to `developers.strava.com` and Website  to `https://www.strava.testapp.com`


## 2- Authorize Credentials in the Browser

Visit web page replacing the client_id to authorize the new Strava App to read data from Strava. You can find the client_id in `https://www.strava.com/settings/api`

http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all

> **Warning**
> Take into acount that the last part of the URL `scope=...` will set the credentials for the APP to read the data I recoomend to use `scope=activity:read_all` more information about each API Request permissions on the [Strava developers APP](https://developers.strava.com/playground/)


## 3- Get Strava Access Code

Once click Authorize it redirects you to a new URL to a URL like this one `http://localhost/exchange_token?state=&code=[code]&scope=read,activity:read_all` where we need to copy the `code` and save.


## 4- Get Strava Access and Refresh Tokens

We want to make an API request to get the **actual access token information** to the following endpoint `https://www.strava.com/oauth/token`

You’ll want to provide the following as query parameters:
- `client_id`: you can get this from your Strava account
- `client_secret`: you can get this from your Strava account
- `code`: you should have received this in the last step from the URL
- `grant_type`: set this to `authorization_code`

The complete URL look like this:
`https://www.strava.com/oauth/token?client_id=xxxxxxx&client_secret=xxxxxxxxxxxxxxxxxxxxxx&code=1c49xxxxxxxxxxxxxxxxxxxxxxx&grant_type=authorization_code`

The important fields to pay attention to here are `expires_at`, `refresh_token`, and `access_token`.

Strava’s `access_token` will expire at the `expires_at` time which is a **Unix Epoch timestamp**. We’ll talk about refreshing later, but for now let’s get some Strava data.




# Links
- Strava Developer Playground [Link](https://developers.strava.com/playground/)