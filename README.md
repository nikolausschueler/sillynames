# README #

### What is it? ###

This is a little demo of how to testing with Selenium
(https://www.seleniumhq.org/). The app presents names which are presumed to be
funny.

### How do I get set up? ###

* Install PhantomJS. Get it from the PhantomJS homepage, http://phantomjs.org/,
  install it and add it to your path.

* Set up the Virtualenv with `make venv`.
* Activate it with `source venv/bin/activate`
* Install needed packages with `pip install -r requirements.txt`
* Run the tests with `make test`

### Docker issues ###

This also contains a Dockerfile. With this, you can create a Docker image, run
it and access the app from your host. But the Docker setup can not run the
tests, there is a problem with PhantomJS that prevents this. Although it looks
like you can install PhantomJS with Node/Npm, I couldn't set it up so the tests
could be run.

### Copyright ###

Copyright (C) 2018 by Nikolaus Schüler, nik@drnik.org.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
