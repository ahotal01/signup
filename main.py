#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

signup_form = """
<form   action="/"
        method="post"
        style="padding:25px; background-color:#d9d9d9; border-radius:10px">
    <label>
        Username:
        <input type="text" name="username" value="%(usr)s"/>
    </label>
    <br>
    <label>
        Password:
        <input type="text" name="password"/>
    </label>
    <br>
    <label>
        Confirm Password:
        <input type="text" name="pass-con"/>
    </label>
    <br>
    <label>
        Email (optional):
        <input type="text" name="email" value="%(eml)s"/>
    </label>
    <br>
    <input type="submit"/>
</form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = signup_form % {"usr": "", "eml": ""}

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        response = page_header + form + page_footer
        self.response.write(response)

    def post(self):
        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        pass_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        username = self.request.get("username")
        password = self.request.get("password")
        pass_con = self.request.get("pass-con")
        email = self.request.get("email")

        input_valid = False

        if username == "" or username.isspace():
            error = "Please provide a username.".format(username)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif not user_re.match(username):
            error = "Invalid username.".format(username)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif password == "" or password.isspace():
            error = "Please provide a password.".format(password)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif not pass_re.match(password):
            error = "Invalid password.".format(password)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif pass_con == "" or pass_con.isspace():
            error = "Please verify your password.".format(pass_con)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif password != pass_con:
            error = "Passwords do not match.".format(password)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        elif email != "" and not email_re.match(email):
            error = "Invalid email.".format(email)
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        else:
            response = "<h1>Welcome, " + username + "!</h1>"
            input_valid = True

        if not input_valid:
            form = signup_form % {"usr": username, "eml": email}

            error = self.request.get("error")
            error_element = "<p class='error'>" + error + "</p>" if error else ""

            main_content = form + error_element
            response = page_header + main_content + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
