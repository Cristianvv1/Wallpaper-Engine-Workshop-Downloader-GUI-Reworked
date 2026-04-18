# Wallpaper Engine Workshop Downloader GUI

A simple tool to download Wallpaper Engine workshop items with a clean interface.

This is a reworked version of the original project with small improvements and an updated GUI.

## Credits

[Original project by SteamAutoCracks](https://gitlab.com/steamautocracks/wallpaperengineworkshopdownloader)

[Additional setup notes by jpgjm](https://github.com/Cristianvv1/Wallpaper-Engine-Workshop-Downloader-GUI-Reworked/issues/1)

## Features

* Download workshop items without using your own Steam account
* Simple and clean interface
* Easy to use

## Requirements

* [DepotDownloaderMod](https://github.com/Cristianvv1/Wallpaper-Engine-Workshop-Downloader-GUI-Reworked/releases/tag/depotdownloadermod)
* [.NET 8.0 Runtime](https://aka.ms/dotnet-core-applaunch?framework=Microsoft.NETCore.App&framework_version=8.0.0&arch=x64&rid=win10-x64)
* [.NET 9.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-9.0.15-windows-x64-installer) 
* Python 3.12
* PyQt6

## Setup

1. [Install .NET 8.0 Runtime](https://aka.ms/dotnet-core-applaunch?framework=Microsoft.NETCore.App&framework_version=8.0.0&arch=x64&rid=win10-x64)

2. [Install .NET 9.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-9.0.15-windows-x64-installer) 

3. Install Python

You can install it manually or use this command:

```
curl -o python-installer.exe https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe
.\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
```

4. Install PyQt6

```
python -m pip install PyQt6
```

## Usage

1. [Open the Wallpaper Engine workshop](https://steamcommunity.com/app/431960/workshop/)

2. Copy the link of the item you want
   Example:
   https://steamcommunity.com/sharedfiles/filedetails/?id=3406264550
   
4. Run the application

5. Paste the link into the app

6. Select your Wallpaper Engine folder
   It must contain the folder `projects/myprojects`

7. Click Download

## Notes

* Make sure the selected path is correct
* Some items may fail depending on availability

## [Tutorial](https://youtu.be/oc8NAviKFD8)

