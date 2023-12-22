# SpotiMeter
SpotiMeter is a command-line interface (CLI) application that utilizes the Spotify API to provide some listening statistics.

## Overview

Using this tool, you can view some of your listening statistics on Spotify, including top tracks, artists, genres and audio features (you can specify time range and limit). Additionally, you can check specific song's audio features.

In order to use SpotiMeter, you need to create a Spotify Developer account, and create an app there. After that, in the SpotiMeter folder, create a file named credentials.json with client_id and client_secret or your app.

```json
{
  "client_id": "123",
  "client_secret": "abc"
{
```

## Getting started

```bash
git clone https://github.com/atlantis-11/SpotiMeter
```

## Installing dependencies

Ensure you have Python3.x installed, and install the required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Make sure to provide --auth option if you run this app for the first time:
```bash
python3 main.py --auth
```

### Options
```
--auth (add this option if you haven't authorized yet and tokens.json file is not present)
--top {tracks,artists,genres,features}
--time-range {short_term,medium_term,long_term} (medium_term by default)
--limit LIMIT (how many items to return, 1 to 50, 20 by default)
--get-features TRACK_ID
```

From [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks):  
- long_term: calculated from several years of data and including all new data as it becomes available.
- medium_term: approximately last 6 months.
- short_term: approximately last 4 weeks.

### Examples
```bash
# Example 1: Get 10 top tracks for the last month
python3 main.py --top tracks --time-range short_term --limit 10

# Example 2: Check audio features for a specific track
python3 main.py --get-features TRACK_ID
```
