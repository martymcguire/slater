Slater
======

Slater is a [micropub](https://www.w3.org/TR/micropub/) client for posting
[events](https://indieweb.org/event) to your website.

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

* Move HTML to templates
* Nice date/time and timezone picker, probably courtesy some http://momentjs.com/ magic.
* Autocomplete support for locations using ... what? how about a page full of
  h-cards with venue information? http://indieweb.org/venue
* Categories: split on commas and strip whitespace and put into `category[]` format
* Support for syndication links from silos
* Support for mp-syndicate-to via micropub config or syndication-to query
* Support for micropub media endpoint for photo
  * upload it
  * replace file field with hidden field w/ Location: URL returned by mp media endpoint
* CORS issues? Use a proxy?
