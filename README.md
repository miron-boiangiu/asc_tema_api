<div id="top"></div>

![Homework][homework-shield]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/miron-boiangiu/asc_tema_api">
    <img src="images/logo.png" alt="Logo" width="120" height="120">
  </a>

<h3 align="center">Le Stats Sportif | ASC Homework</h3>

  <p align="center">
    First ASC Homework - API for sports stats.
    <br />
    <br />
    <a href="https://github.com/miron-boiangiu/asc_tema_api/issues">Report Bug</a>
    ·
    <a href="https://github.com/miron-boiangiu/asc_tema_api/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#logging">Logging</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Simple Flask API that asynchronously computes and replies to requests.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python 3](https://www.python.org/doc/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

* [Python 3](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Structure

#### ThreadPool

ThreadPool has a generic Task that is meant to be inherited from and modified according to the particular context in which it is to be used.

Its TaskRunners (which run in their own threads) continuously poll the ThreadPool for new tasks to execute and can be shut down by shutting down the parent ThreadPool itself.

#### Handling requests

In Flask view functions, requests are parsed and sent to an instance of QueryHandler, whose job is to transform the query's data into a specific Task instances that are then passed to the ThreadPool to execute.

Subjects later send another request to the API to check whether or not a previous query has finished, in which case the result is fetched and sent back.

<br>
<p align="right">(<a href="#top">back to top</a>)</p>

## Logging

All requests are logged in *webserver.log*, with a max size of 200KB, the file is rotated when the size is reached and up to 5 rotations are kept.

<br>
<p align="right">(<a href="#top">back to top</a>)</p>

## Testing

Since the checker basically acts like integration tests, in the unit tests I decided not to test the routes themselves but the general behaviour of the classes I added.

<br>
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Boiangiu Victor-Miron - miron.boiangiu@gmail.com

Project Link: [https://github.com/miron-boiangiu/asc_tema_api](https://github.com/miron-boiangiu/asc_tema_api)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/miron-boiangiu/streaming_platform.svg?style=for-the-badge
[contributors-url]:https://github.com/miron-boiangiu/asc_tema_api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/miron-boiangiu/streaming_platform.svg?style=for-the-badge
[forks-url]:https://github.com/miron-boiangiu/asc_tema_api/network/members
[stars-shield]: https://img.shields.io/github/stars/miron-boiangiu/streaming_platform.svg?style=for-the-badge
[stars-url]:https://github.com/miron-boiangiu/asc_tema_api/stargazers
[issues-shield]: https://img.shields.io/github/issues/miron-boiangiu/streaming_platform.svg?style=for-the-badge
[issues-url]:https://github.com/miron-boiangiu/asc_tema_api/issues
[license-shield]: https://img.shields.io/github/license/miron-boiangiu/streaming_platform.svg?style=for-the-badge
[license-url]:https://github.com/miron-boiangiu/asc_tema_api/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/miron-boiangiu
[product-screenshot]: images/screenshot.png
[homework-shield]: https://img.shields.io/badge/UPB-Homework-%23deeb34?style=for-the-badge

