
# CI/CD Deployment Documentation

## Overview

This project uses GitHub Actions to automate Continuous Integration and Continuous Deployment.

## Continuous Integration

The CI pipeline performs the following checks:

1. Checks out the repository.
2. Validates project documentation.
3. Sets up Python 3.12.
4. Runs five automated calculator tests.

## Continuous Deployment

After successful CI checks on the main branch:

1. GitHub Actions prepares the website.
2. Website files are uploaded as a Pages artifact.
3. GitHub Pages deploys the website.


## Trigger

- Push to main: Runs CI and deployment.
- Pull request targeting main: Runs CI checks.
- Deployment only occurs on pushes to main.

## Hosting

The website is hosted using GitHub Pages.
