Slater
======

Slater is a [micropub](https://www.w3.org/TR/micropub/) client for posting
[events](https://indieweb.org/event) to your website.

**Notice 2024-10: This project has been superceded by [Slater-PHP](https://git.schmarty.net/schmarty/slater-php).** Please see the new project for updates. This version is no longer maintained.

Quick (&amp; Dirty) Start
-------------------------

Create and activate a virtualenv:

	virtualenv --python=/usr/bin/python3 venv
	source venv/bin/activate

or conda:

	conda create -n slater python=3.5
	source activate slater

Install required Python libraries

	pip install -r requirements.txt

Run the dev server

	python slater.py

View the app in your browser at `http://localhost:5000`.

TODOs
-----

So many.

* Autocomplete support for locations using ... what? how about a page full of
  h-cards with venue information? http://indieweb.org/venue
* Automatic timezone selection?
	* once date/time and location (even approx) are known, can find proper
	  timezone.
		* [Atlas does this](http://atlas.p3k.io/)
		* Could also guess from [the browser's local tz](https://stackoverflow.com/questions/1091372/getting-the-clients-timezone-in-javascript) + event time
		* could dig into [W3C best practices for timezones](https://www.w3.org/TR/timezone/#negotiating)
			* [tzinfo](http://www.twinsun.com/tz/tz-link.htm)
			* [CLDR](http://cldr.unicode.org/)
* Categories: split on commas and strip whitespace and put into `category[]` format
* Support for syndication links from silos
* CORS issues? Use a proxy?
