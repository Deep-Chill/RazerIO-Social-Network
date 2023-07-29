# RazerIO

:star: Star it on GitHub!

RazerIO is a social network for professionals built with Django. I don't care about the design, I've only made the backend.

<a href="https://ibb.co/HDSsQfr"><img src="https://i.ibb.co/5W0yVg5/Screenshot-7.png" alt="Screenshot-7" border="0"></a>

## Table Of Content

- [Installation](#installation)
    - [Installation](#installation)
    - [Getting started](#getting-started)
- [Features](#Features)
    - [Account](#account)
    - [Social Feeds](#social-feeds)
    - [Messaging](#messaging)
    - [Company Page](#company)
    - [Job board](#job-board)
    - [Company](#company)
- [Incomplete tasks](#page-setup)
    - [Download the Aimeos Page Tree t3d file](#download-the-aimeos-page-tree-t3d-file)
    - [Go to the Import View](#go-to-the-import-view)
    - [Upload the page tree file](#upload-the-page-tree-file)
    - [Go to the import view](#go-to-the-import-view)
    - [Import the page tree](#import-the-page-tree)
    - [SEO-friendly URLs](#seo-friendly-urls)
- [License](#license)
- [Links](#links)

## Installation

To install razerIO, ensure you have Python 3.8 or higher installed on your system. Clone this repository, navigate to the project directory and run the following commands:

```sh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Getting started
After successfully installing and running the server, navigate to http://localhost:8000 on your browser to access the razerIO homepage. To start using razerIO, register for a new admin account by running the command: 
```
python manage.py createsuperuser
```
then use credentials created there to login. You can then logout and create new user accounts with Google or Github.

## Features

## Account
Sign up using Google or Github. Follow/Unfollow users. Profile page with personal information, company information, employment history, endorsements from colleagues, and more. Tweak your profile by changing settings, update your email/passwords, remove connected social media accounts or change your bio/picture. Get profile tags such as a verified company tag if you're a verified employee.

<a href="https://imgbb.com/"><img src="https://i.ibb.co/zm0Vq7Y/Screenshot-15.png" alt="Screenshot-15" border="0"></a>
<hr><br>
<a href="https://ibb.co/n1zRTxx"><img src="https://i.ibb.co/hdDCk33/Screenshot-8.png" alt="Screenshot-8" border="0"></a>
<hr><br>

## Social Feeds
3 social feeds, one for your friends list, one for everyone in the same company as you, and one for everyone in the same country as you.
<a href="https://ibb.co/HDSsQfr"><img src="https://i.ibb.co/5W0yVg5/Screenshot-7.png" alt="Screenshot-7" border="0"></a>
<hr><br>

## Messaging
Create group threads with up to 50 members. Send and receive messages from people in yours friends list. Receive alerts for events (new friend requests, comments on newspaper articles, and more!)

<a href="https://ibb.co/WfYvcMR"><img src="https://i.ibb.co/SB9wKMZ/Screenshot-9.png" alt="Screenshot-9" border="0"></a>
<hr><br>

## Company Page
Find your company in a list of provided companies. Can't find it? Create your own! If the company is public, provide the stock ticker and the website will automatically fill in the rest. If it's private, provide information you want to go on there. Get a verified employee tag so you can create job listings for the company and post in the company's social feeds. 

The company page includes financial information about the company, ownership(and if those owners are in RazerIO it directly links to their profiles,) available job openings, and more information sourced by verified employees on the platform.

<a href="https://ibb.co/pn72rJG"><img src="https://i.ibb.co/BwpLKqd/Screenshot-14.png" alt="Screenshot-14" border="0"></a>


## Job board
If you're looking for a job: Search and filter for jobs, apply for jobs, and keep track of your applications.

If you're hiring: Create new job listings for your company, manage listings, and keep track of applicants.

<a href="https://ibb.co/D8D7nHC"><img src="https://i.ibb.co/cCcNdSF/Screenshot-10.png" alt="Screenshot-10" border="0"></a>
<hr><br>

<a href="https://ibb.co/ZTnmcfw"><img src="https://i.ibb.co/7yw4rST/Screenshot-11.png" alt="Screenshot-11" border="0"></a>
<hr><br>
<a href="https://ibb.co/TkbKnwq"><img src="https://i.ibb.co/wRwJbdr/Screenshot-12.png" alt="Screenshot-12" border="0"></a>
<hr><br>
<a href="https://ibb.co/QjCkC66"><img src="https://i.ibb.co/84dbdjj/Screenshot-13.png" alt="Screenshot-13" border="0"></a>
<hr><br>
<hr><br>
