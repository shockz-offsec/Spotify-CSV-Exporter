
# Spotify CSV Exporter

This tool performs automated and organized exports of Spotify playlists and favorite songs in CSV format, leveraging the Sportify project.

Can run on both Windows and Linux

> !! At no time is the information (credentials) used in the script are recompiled.!!

## Requirements & Installation

To use this tool, you need to have the Selenium module installed. You can install it by running the following command in your terminal:

```bash
pip install selenium requests
```

After that, you can download the repository by running the following commands:

```bash
git clone https://github.com/shockz-offsec/Spotify-CSV-Exporter.git
cd Spotify-CSV-Exporter
```

### Compatibility

This script is compatible with both Windows and Linux operating systems and requires Python 3.

## Configuración

The script's configuration is defined in the config_spotify.json file, which has the following structure:

```json
{
    "DOWNLOAD_PATH": "C:\\path\\to\\your\\backups",
    "DEBUG_PATH": "C:\\path\\to\\your\\logs",
    "EMAIL":"your_spotify_email",
    "PASSWORD":"your_password"
}
```

* `DOWNLOAD_PATH`: the path where the downloaded files will be stored.
* `DEBUG_PATH`: the path where the script logs will be saved.
* `EMAIL`: the email address associated with the Spotify account.
* `PASSWORD`: the password associated with the Spotify account.

## Usage

```bash
python3 spotify_backup.py
```

## Importing Backups into Spotify again

To achieve this, you just need to open the CSV file of each playlist and extract the values from the "Track URI" column.

This can be done by opening the CSV file with Excel and then navigating to Data => Text to Columns => Next => Delimited (Next) => Comma (Next) => Finish.

![CSV](https://github.com/shockz-offsec/Spotify-CSV-Exporter/assets/67438760/ab0a0f1d-066d-4898-97a9-77e97b04b593)

Next, simply copy all the Track URIs using Ctrl+C and paste them into a playlist in Spotify Desktop using Ctrl+V.


## Automating backups

In Windows, you can automate the script by creating a scheduled task with the Windows Task Scheduler. This can be done by creating a `.bat` file with the following contents:

```batch
@echo off
C:\Python3\python.exe "C:\path\to\spotify_backup.py"
```
This will allow the script to run automatically at specified intervals without requiring manual intervention.

In Linux you can use Cron for example.
