# GitNuff
An exceedingly lightweight frontend for GitHub that just shows README's and
ways to get the code. It's designed to be used with lightweight browsers like
lynx, neosurf, netsurf, or w3m that can't handle GitHub's fancy JavaScript
based UI.

## Installation and Usage
1. Clone
  ```
  git clone https://github.com/thavelick/gitnuff && cd gitnuff
  ```
2. Start the server
  ```bash
  ./gitnuff.py
  ```
3. Open your browser to http://localhost:8009/someorg/somerepo

### Environment variables
* `GITNUFF_PORT`: The http port to run on. Defaults to 8009
* `GITNUFF_GITHUB_PERSONAL_TOKEN`: (optional, but recommended)
  if set, this will use the token to make requests to the GitHub API.
  This allows 2500-5000 requests per hour.
  Since it can get all the data needed in 1-2 API requests, this using a token
    is significantly faster than not using one.
  To get a token, see:
    [Managing Your Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  When omitted, GitNuff will make several HEAD requests to verify the repo's
    existence before pulling down the README. I'm not sure what rate limits
    github has here.

## Urls
The urls should mostly correspond to github.com ones, so you can replace https://github.com with http://localhost:8009/ and it will work.

## Dependencies
* Python 3.x

## Created By
* [Tristan Havelick](https:/tristanhavelick.com)
