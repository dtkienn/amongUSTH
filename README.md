# amongUSTH

**1. INTRODUCTION**

Among USTH is a question and answer site to help USTH students with their academic study. 

**2. FEATURES**

* Login feature
    Students are required to login with their given school mail addresses.

* Ask and answer pages
    Students are able to create a discussion to give questions, and also able to answer to others' discussions.

* Books sharing
    Students are able to upload books related to courses. These books should be verified by administrators before being approved.

* Profile pages (?)
    This page should combines all activities of one account on website.
    This includes person's name, schoolyear and submitted questions and answers.

**3. TECHNOLOGY**

	Python with Framework Flask

	Languages included:

* Python
* HTML, CSS, JS
* MySQL

**4. USAGE**

	pip install virtualenv
	python app.py then follow route on browser

**5. DEVELOPING PROCESS** (by team leader, any comments of team members are taken into consideration)

Processes should be divided in weeks for better tracking. 

These targets should be adjusted every two weeks to address real-time problems with the project and re-decide team's priority if needed.

- 1st week: Frontend: Create html base templates for the website, therefor create some fundamental html sites.
		+ Created templates: homepage, profile, sign in.
            Backend: Create google login function, initiate database.
		+ Process: login function added, however no options for logging out. *NEED MORE WORK ON THIS*
			   database: 
	
- 2nd week: Frontend: Continue developing html sites, start enhancing page looks, and further design and contents
		+ May need artwork and sublime content writing for the page.
		+ To-build html sites: discussion page, all_discussion page (where all discussions of the page are loaded), ...
	    Backend: Finish google login function (priority), develop database (schema and queries)
	        + Develop and debug google login
		+ Develop deeper and larger database for the site. *NEEDS FURTHER RESEARCH*
		
- 3nd week: Frontend: Continue developing html sites, start enhancing page looks, and further design and contents
		+ May need artwork and sublime content writing for the page.
		+ To-build html sites: book-related pages, determine the most optimal way to present user-friendly pages.
	    Backend: 
	    	+ Create file (books) upload and download function, preview function (optional)
	    	+ Start displaying database information in pages
		
- 4nd week: ....
		



