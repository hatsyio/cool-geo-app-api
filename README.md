<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/hatsyio/cool-geo-app-api">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Cool geo app API</h3>

  <p align="center">
    API to provide service to cool geo app
    <br />
    <a href="https://github.com/hatsyio/cool-geo-app-api"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hatsyio/cool-geo-app-api">View Demo</a>
    ·
    <a href="https://github.com/hatsyio/cool-geo-app-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/hatsyio/cool-geo-app-api/issues">Request Feature</a>
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
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running-the-tests">Running the tests</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Cool geo app API Screen Shot][product-screenshot]

API to serve cool geo app, point here to access the services needed by the frontend in order to retrieve data and manage
give service to the application.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [Poetry](https://python-poetry.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [PostGIS](https://postgis.net/)
* [Docker](https://www.docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

The software needed to run the project is

* Running standalone:
  * git
  * Docker
  * docker-compose

  _run standalone with the next command_
  ```sh
  docker-compose --profile cool-geo-app-api up
  ```
Access http://127.0.0.1:8080/docs through your browser.

### Installation

Running directly on your machine.

If you want to run the project directly on your machine for development purposes you will also need poetry.
```sh
pip install poetry
```

0. Setup pre-commit framework
   ```sh
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

1. Clone the repo
   ```sh
   git clone https://github.com/hatsyio/cool-geo-app-api.git
   ```
2. Install poetry packages
   ```sh
   poetry install
   ```
3. Set up database
    ```shell
    docker-compose up
    ```

4. Set env variables
   ```sh
   export DB_HOST="postgres"
   export DB_PORT="5432"
   export DB_USER="postgres"
   export DB_PASSWORD="postgres"
   export DB_NAME="cool-geo-app"
   ```

5. Tell poetry to run the project
   ```shell
   poetry run uvicorn app.main:app --host 127.0.0.1 --port 8080
   ```

### Running the tests
You can also use poetry to run the tests.
   ```shell
   poetry run pytest
   ```
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Mainly the API is divided between two modules Payments which is responsible for paystats data and PostalCodes which is
responsible for postal codes data.

### Payments

The idea around Payments module is let you play with the data at the aggregation level that you want.

For that you will have endpoint to query the dimensions (ages, genders, months) and an aggregation endpoint to request
the aggregation at the level that you want. You can filter by the specified parameters and also do not filter at all but
add the desired fields at the aggregation result.

The response would be like the output of a group by call to a database in json response format.
It will always return an amount.

You have fine-grained endpoints like time-series and postal-codes endpoints which will enforce the fields of p_month and postal-code to be
present on the result, and enforce you to specify a time range or a postal-code depending on the endpoint.

### PostalCode

This module is for returning postal code data, you can query for all the postal codes, look for specific ones and also
ask for a union of geometries of two postal codes.

Endpoints are described in more detail in the api [docs](http://localhost:8080/docs)

For more examples, please refer to the [Documentation]

_Replace link placeholder for confluence, gitbook, etc._

### Authorization

Added authorization, please sign up as a user and login to get access to the API.
you need to request a bearer token with the following endpoint:

    POST /authorization/token

    {
        "username": "username",
        "password": "password",
        "scopes": "payments postal-codes"
    }

Scope payments is used for payments endpoints and scope postal-codes is used for postal-codes endpoints.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Architecture -->
## Architecture

We will be using a classic 3 Tier Application architecture, where the modules would be routers, services and database,
each one of them decoupled of each other, and receiving the requests on the routers module.

The only module allowed to speak with the postgresql database would be database.

![Architecture diagram][architecture-diagram]

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [X] Postal codes endpoints
  - [X] Aggregated postal codes geometries endpoint
- [X] Payments endpoints
- [X] Cache
- [ ] CI/CD
- [ ] Authorization
- [ ] Model version control (Liquibase)

See the [open issues](https://github.com/hatsyio/cool-geo-app-api/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Josep Pascual Badia - joseppascualbadia@gmail.com

Project Link: [https://github.com/hatsyio/cool-geo-app-api](https://github.com/hatsyio/cool-geo-app-api)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best Readme template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/hatsyio/cool-geo-app-api.svg?style=for-the-badge
[contributors-url]: https://github.com/hatsyio/cool-geo-app-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hatsyio/cool-geo-app-api.svg?style=for-the-badge
[forks-url]: https://github.com/hatsyio/cool-geo-app-api/network/members
[stars-shield]: https://img.shields.io/github/stars/hatsyio/cool-geo-app-api.svg?style=for-the-badge
[stars-url]: https://github.com/hatsyio/cool-geo-app-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/hatsyio/cool-geo-app-api.svg?style=for-the-badge
[issues-url]: https://github.com/hatsyio/cool-geo-app-api/issues
[license-shield]: https://img.shields.io/github/license/hatsyio/cool-geo-app-api.svg?style=for-the-badge
[license-url]: https://github.com/hatsyio/cool-geo-app-api/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/josep-pascual-badia-14a199a2
[product-screenshot]: images/screenshot.PNG
[architecture-diagram]: images/diagram.png
