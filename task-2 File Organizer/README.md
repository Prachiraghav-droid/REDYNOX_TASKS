# Automated File Organizer

## Project Overview

The Automated File Organizer is a Python automation tool designed to solve the repetitive task of manually sorting files into folders.

The program identifies files based on their extensions and automatically moves them into appropriate categories.

## Problem Statement

Managing a folder containing many different types of files can become repetitive and time-consuming.

For example, images, documents, videos, audio files, and code files may all be stored in the same folder.

Manually organizing these files requires repeated effort.

## Solution

This project automates the organization process.

The program:

1. Accepts a folder path from the command line.
2. Scans the files inside the folder.
3. Identifies each file based on its extension.
4. Creates category folders automatically.
5. Moves files into the appropriate folders.
6. Creates a log of the operations.
7. Displays a summary of the files organized.

## File Categories

The program currently supports:

- Images
- Documents
- Videos
- Audio
- Archives
- Code
- Others

## Technologies Used

- Python 3
- `os`
- `shutil`
- `logging`
- `argparse`

These are standard Python libraries, so no external packages are required.

## Project Structure

```text
redynox-task-2-file-organizer/
│
├── file_organizer.py
├── README.md
└── file_organizer.log