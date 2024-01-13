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

## Urls

The urls should mostly correspond to github.com ones, so you can replace https://github.com with http://localhost:8009/ and it will work.

## Dependencies
* Python 3.x


## Created By
* [Tristan Havelick](https:/tristanhavelick.com)
