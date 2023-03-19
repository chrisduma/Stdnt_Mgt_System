<!-- Back to Top Navigation Anchor -->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<!-- <img src="(https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_1.PNG)" width="50%"/>
<img src="(https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_2.PNG)" width="50%"/>
<img src="(https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_3.PNG)" width="50%"/>
<img src="(https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_4.PNG)" width="50%"/>
<img src="(https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_5.PNG)" width="50%"/> -->


<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
</div>

<!-- Project Name -->
<div align="center">
  <h1>Student_Management_System</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/ChrizDuma/Stdnt_Mgt_System#readme"><strong>Explore the Docs »</strong></a>
    <br />
    <a href="https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_3.png">View Testing</a>
    ·
    <a href="https://github.com/ChrizDuma/Stdnt_Mgt_System/issues">Report Bug</a>
    ·
    <a href="https://github.com/ChrizDuma/Stdnt_Mgt_System/issues">Request A Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-Stdnt_Mgt_System">About Stdnt Mgt System</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Project -->
## About The Student Management API

A restful API which enables an admin to register accounts for both students and admins, as well as manage the database load from the data collected. CRUD operations can be performed on all accounts created within this API. The python pytest package has been used for testing as well as debugging of this api, among other softwares such as swagger UI and Insomnia.

It works in a way that Students have limited access to the app as opposed to the admins.
A student can only change their profile details and view their profile, courses, grades and CGPA.
Overall access is granted to the admins.

This student management API was built with Python's Flask-RESTX by <a href="https://www.github.com/ChrizDuma">Chris Duma</a>.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Lessons Learned

Creating this API helped me learn and practice:
* API Development with Python
* App Deployment with PythonAnywhere
* Testing with pytest and Insomnia
* Documentation
* Debugging
* Routing
* Database Management and Adminstration
* Internet Security
* User Authentication & Authorization

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To use this API, follow these steps:

1. Open the PythonAnywhere web app on your browser: https://chrisduma.pythonanywhere.com

2. Create an admin or student account:
    - Click 'admin' to reveal a dropdown menu of administration routes, then register an admin account via the '/admin/register' route
    - Click 'students' to reveal a dropdown menu of student routes, then register a student account via the '/students/register' route

3. Sign in via the '/auth/login' route to generate a JWT token. Copy this access token.

4. Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, for example:
  
  ``` Bearer this1is2a3rather4long5hex6string ```

5. Click 'Authorize' and then 'Close'

6. Now authorized, you can create, view, update and delete students, courses, grades and admins via the many routes in 'students', 'courses' and 'admin'. You can also get:
7.  - All users of the APP (Admins & Students included)
    - All students taking a course
    - All courses taken by a student
    - A student's grades in percentage (eg: 84.8%) and letter grades (eg: A+)
    - A student's CGPA, calculated based on all grades from all courses they are taking

7. When you're done, click 'Authorize' at top right again to then 'Logout'

  **Note:** When using this API in production, please [fork this repo](https://github.com/ChrizDuma/Stdnt_Mgt_System) and uncomment the `@is_admin()` decorator in line 60 of [the admin views file](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/api/routes/admin_views.py). This will ensure that students and other users will not be authorized to access the admin creation route after the first admin is registered, in other words, first Admin gives access to new admins.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

![Capture 1](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_1.PNG)
![Capture 2](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_2.PNG)
![Capture 3](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_3.PNG)
![Capture 4](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_4.PNG)
![Capture 5](https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Capture_5.PNG)



<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/Ze-Austin/ze-school/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

Chris Duma - [@ChrisDuma3](https://twitter.com/Chris Duma) - chrisduma01@yahoo.com

Project Link: [Stdnt_Mgt_System](https://github.com/ChrizDuma/Stdnt_Mgt_System)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [Chris Duma](https://github.com/ChrizDuma)
* [Caleb Emelike](https://github.com/CalebEmelike)
* [Austin Wopara](https://github.com/Ze-Austin)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/ChrizDuma/Stdnt_Mgt_System.svg?style=for-the-badge
[contributors-url]: https://github.com/ChrizDuma/Stdnt_Mgt_System/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ChrizDuma/Stdnt_Mgt_System.svg?style=for-the-badge
[forks-url]: https://github.com/ChrizDuma/Stdnt_Mgt_System/network/members
[stars-shield]: https://img.shields.io/github/stars/ChrizDuma/Stdnt_Mgt_System.svg?style=for-the-badge
[stars-url]: https://github.com/ChrizDuma/Stdnt_Mgt_System/stargazers
[issues-shield]: https://img.shields.io/github/issues/ChrizDuma/Stdnt_Mgt_System.svg?style=for-the-badge
[issues-url]: https://github.com/ChrizDuma/Stdnt_Mgt_System/issues
[license-shield]: https://img.shields.io/github/license/ChrizDuma/Stdnt_Mgt_System.svg?style=for-the-badge
[license-url]: https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@ChrisDuma3-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/ze_austin
[twitter-url]: https://twitter.com/ChrisDuma3
[ze-school-screenshot]: https://github.com/ChrizDuma/Stdnt_Mgt_System/blob/main/images/Ze_School_Full_Page.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
