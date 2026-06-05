<header align="center">
  <h1>
    <img src="assets/img/title.png" alt="Title">
  </h1>
  <img src="assets/img/screenshot.png" alt="Screenshot of Highland Highlights">
</header>

## About

As a student, I developed Highland Highlights, a Raspberry Pi-powered digital signage application written in Qt for Python, to replace the old TVs' information display at Highland High School. It introduces a new design and displays the Word documents and PDFs that staff and clubs already create.

## Features

- **Clock & Date**: Displays the current time and date
- **Local Weather**: Displays the current condition and temperature
- **Weekly Announcements**: Scrolls through formatted text from a Word document
- **Club Advertisements**: Cycles through slides from a PDF

## Setup

1. Create an account and get a free API key from [weatherapi.com](https://www.weatherapi.com). This is required for the Local Weather & Temperature feature.
2. Clone Highland Highlights.
3. Run [setup.sh](sripts/setup.sh) in the terminal and follow its instructions.
4. Download the Weekly Announcements Microsoft Word file shared with you by Desiree Chavez from your Google Drive.
5. Prepare a slideshow with the dimensions 1920x810px for the Club Advertisements and export it as a PDF document. Each slide should be a separate page.
6. Move the Microsoft Word and PDF files into the "documents" folder inside `highland-highlights/assets`.

## Usage

- To run Highland Highlights, run [run.sh](scripts/run.sh).
- To change the Weekly Announcements or Club Advertisements on screen, move your Microsoft Word and PDF document into the documents folder. The screen will automatically refresh without a restart of the application.

## Customization

To customize the appearance and behavior of Highland Highlights, modify the values of the constants in [config.py](highland-highlights/config.py).

> [!NOTE]
> Sizes, widths, heights, and spacing are measured in pixels; intervals are measured in milliseconds.
