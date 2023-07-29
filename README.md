# RazerIO

:star: Star it on GitHub!

RazerIO is a social network for professionals built with Django. Think LinkedIn but for computer scientists and programmers. I don't care about the design, I've only made the backend.

<a href="https://ibb.co/HDSsQfr"><img src="https://i.ibb.co/5W0yVg5/Screenshot-7.png" alt="Screenshot-7" border="0"></a>

## Table Of Content

- [Installation](#installation)
    - [Installation](#installation)
    - [Getting started](#getting-started)
- [Features](#Features)
    - [Account](#account)
    - [Social Feeds](#social-feeds)
    - [Messaging](#messaging)
    - [Company Page](#company-page)
    - [Job board](#job-board)
    - [Leaderboards](#leaderboards)
    - [Projects](#projects)
    - [Newspaper](#newspaper)
- [Planned Features](#planned-features)
    - [New Modules](#new-modules)
    - [Module Improvements](#module-improvements)
    - [Security](#security)
    - [Non-Essential Features](#non-essential-features)
    - [Long-Term Features](#long-term-features)
    - [Pre-production Tasks](#pre-production-tasks)
- [License](#license)
- [Contribute](#contribute)

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
Sign up using Google or Github. Follow/Unfollow users. Profile page with personal information, company information, employment history, endorsements from colleagues, and more. Tweak your profile by changing settings, update your email/passwords, remove connected social media accounts or change your bio/picture. Get profile tags such as a verified company tag if you're a verified employee. Search for users, articles, and companies in the search bar.

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

The company page includes financial information about the company, ownership(and if those owners are in RazerIO it directly links to their profiles,) available job openings, and more information sourced by verified employees on the platform. Leave reviews anonymously if you're a verified employee.

<a href="https://ibb.co/pn72rJG"><img src="https://i.ibb.co/BwpLKqd/Screenshot-14.png" alt="Screenshot-14" border="0"></a>


## Job board
If you're looking for a job: Search and filter for jobs, apply for jobs, and keep track of your applications. The job board is cached to make the search fast.

If you're hiring: Create new job listings for your company, manage listings, and keep track of applicants. 

<a href="https://ibb.co/D8D7nHC"><img src="https://i.ibb.co/cCcNdSF/Screenshot-10.png" alt="Screenshot-10" border="0"></a>
<hr><br>

## Leaderboards
Ranks companies based on a formula that assigns them a "IO score" which is a score based on valuations such as financials, reviews, and more!

The IO Company score reflects a comprehensive evaluation of the company's financials, stability, global reach, R&D, market share, product diversity, public sentiment, employee satisfaction, ESG score, future outlook and more. Improve your company's IO score by leaving reviews.

<a href="https://ibb.co/ZTnmcfw"><img src="https://i.ibb.co/7yw4rST/Screenshot-11.png" alt="Screenshot-11" border="0"></a>
<hr><br>

## Projects
Showcase your projects or find people to work on them with you. Create new projects, manage existing projects, or apply for a project!

<a href="https://ibb.co/TkbKnwq"><img src="https://i.ibb.co/wRwJbdr/Screenshot-12.png" alt="Screenshot-12" border="0"></a>
<hr><br>

## Newspaper
Create a newspaper, write articles that show up on the homepage feed for everyone in your country. Leave comments on articles anonymously and only choose to show your verified company if you wish. 

<a href="https://ibb.co/QjCkC66"><img src="https://i.ibb.co/84dbdjj/Screenshot-13.png" alt="Screenshot-13" border="0"></a>
<br>
<a href="https://ibb.co/PmQJ82s"><img src="https://i.ibb.co/5MFCVQX/Screenshot-6.png" alt="Screenshot-6" border="0"></a>
<br>
<a href="https://ibb.co/5hJgrWx"><img src="https://i.ibb.co/9Hdkb93/Screenshot-7.png" alt="Screenshot-7" border="0"></a>
<hr><br>

### Planned features

## New Modules

While most of the fundamental features are complete, there's a lot yet to be done.

1. **Competitive Programming Competitions:** A platform for users to engage in competitive programming events with features for companies to host their own programming competitions.
2. **Startups:** A dedicated module offering a suite of features catered towards startups.
3. **Contracts and Internships:** A better system to manage contract work and internships.
4. **Wiki Pages for Organizations/Companies:** Detailed, user-editable wiki pages for companies and organizations.
5. **Groups:** A module to handle group creation and management for team collaborations.

## Module Improvements

### Jobs, Social, Newspaper, Entrepreneurship, Competitive Programming, Testing, and Statistics

- Enhanced features for startups, projects, and competitive programming.
- New competitive programming and testing page.
- Improved statistics with leaderboards for startups, users, and newspapers.
- Integration of something akin to an Elo rating system to user profiles that takes into account their work experience, projects, connections, papers published, and more.


## Security

- Reporting functionality.
- Automatic image resizing.
- New user interface for non-signed in users and sidebar for logged-in users.
- A server limit for file uploads set to 20 MB.
- A distributed scheduling system for API calls to prevent overload.
- Caching mechanisms to reduce API calls and improve response times.


## Non-Essential Features

Additional features to improve existing modules like jobs, social, newspaper, and entrepreneurship. These include but are not limited to, discussion sections on job pages, company health indicators, a freelancing market, and more. Detailed specifications have not been provided.

## Long-Term Features

- Interface dark mode.
- User-friendly navigation persistence.
- Moderation system with scoring for user engagement.
- Stock data visualization.
- Centralized notification system.
- Service marketplace (mentorship, coaching, code review, training, etc.).
- Visualization of user connection webs.

## Pre-production Tasks

- Implementation of an auto-delete function for job listings after 14 days, using Celery. 

Please note that this is a high-level overview, and detailed specifications for each feature and module can be found by reaching out.


## License

RazerIO is licensed under the terms of the MIT License and is available for free.

## Contributing

If you're thinking about using or even contributing to razerIO, feel free to use this code in any way you see fit.

If you spot any bugs, have an idea for an improvement, or even want to add a new feature, go ahead and do it. I'd appreciate if you could report any bugs or suggestions through the [Issue Tracker](https://github.com/razerIO/razerIO/issues).

If you've written code that fixes a bug or adds a new feature, you can create a pull request. A brief description of what you've done and why would be helpful.

Thanks for your interest in RazerIO and happy coding!
