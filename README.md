# ducc
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Harel56/ducc)](https://github.com/Harel56/ducc/releases/latest)
[![Build Status](https://travis-ci.com/Harel56/ducc.svg?branch=master)](https://travis-ci.com/Harel56/ducc)  
[![GitHub followers](https://img.shields.io/github/followers/Harel56?label=Follow&style=social)](https://github.com/Harel56/followers)
[![GitHub forks](https://img.shields.io/github/forks/Harel56/ducc?style=social)](https://github.com/Harel56/ducc/fork)
![GitHub stars](https://img.shields.io/github/stars/Harel56/ducc?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Harel56/ducc?style=social)  
Final project for course advanced system design  

## Download

### From Source

![GitHub repo size](https://img.shields.io/github/repo-size/Harel56/ducc)  

1. Run `git clone https://github.com/Harel56/ducc.git` (or
   clone [your own fork](https://github.com/Harel56/ducc/fork)
   of the repository)
2. Go into the cloned folder with `cd ducc`

### Packaged Distributions

[![GitHub All Releases](https://img.shields.io/github/downloads/Harel56/ducc/total)](https://github.com/Harel56/ducc/releases/latest)

1. Download `ducc-<version>.zip` (or
   `.tar.gz`) attached to
   [latest release](https://github.com/Harel56/ducc/releases/latest)
3. Unpack and `cd` into the unpacked folder

## Project Specification
Project specification can be found at
https://docs.google.com/document/d/1AO_RGoPiMQKQuKFt8E-IwjKXxxt9vnobH-0hfFAxGaQ  

## Quick Deployment
1. Make Sure you have [Docker](https://www.docker.com/) installed
2. Download the project using one of the options described above
3. Go into the project directory with `cd`
4. Deploy the server and its componenents with docker
   using the script at `scripts/run-pipeline.sh` (May take a while)
5. You can upload a sample to the server by running
   `python -m ducc.client upload-sample <sample>` (A sample example
   can be downloaded from [here](https://storage.googleapis.com/advanced-system-design/sample.mind.gz))
6. You can access the GUI by browsing http://localhost:8080

## Background
This project was made by me (Harel Etgar)  
Made for the course "Advanced System Design", Academic year 2019-2020 semester A, [Tel Aviv University](http://www.tau.ac.il/)  
Course Instructor: [Dan Gittik](https://www.dan-gittik.com/)  
Prepared mainly during the COVID-19 outbreak of 2020
