# Applied Predictive Modeling Projects

## Project Description

This repository contains solutions and explorations based on *Applied Predictive Modeling* by Max Kuhn and Kjell Johnson. While the original book uses R, all work here is implemented in Python.

The project is intended for educational purposes—for myself and for readers who want to follow the book but prefer working in Python. For that reason, the implementation is structured as a series of Jupyter Notebooks, making it easy to explore, modify, and visualize code step by step.

This is **not** a strict line-by-line translation of the R code. Many chapters include extended analysis, custom helper functions, or additional visualizations that go beyond the original material—either because they offered good learning opportunities or were personally interesting to explore.

The repository is a work in progress and will continue to be updated as I move through the source material.

## Table of Contents

- [Purpose](#purpose)
- [Environment Setup](#environment-setup)
- [Repository Structure](#repository-structure)
- [Data Access](#data-access)

## Purpose

The goal of this project is to deepen my understanding of predictive modeling techniques by reproducing and expanding on the exercises from *Applied Predictive Modeling* using Python. 

## Project Status

This repository is a work in progress. Notebooks and content will be added and refined continuously as I work through the chapters in *Applied Predictive Modeling*.

## Getting Started

To get started, clone the repository and set up the Conda environment:

```bash
git clone https://github.com/KABOSScodes/apm_projects.git
cd apm_projects
conda env create -f apm_projects_env.yml
conda activate apm_projects
```

*Note:* The environment file is provided for convenience but may occasionally lag behind the current environment, as updates are made continuously throughout the project. If you encounter missing packages, installing them manually post envrionment activation with conda or pip should resolve the issue. 

Additionally, it should be noted that the repository is currently structured with relative paths. For smooth execution of notebooks, ensure the working directory remains the project root when running Jupyter.

## Repository Structure

| Folder/File              | Description |
|--------------------------|-------------|
| `chapters/`              | Utility functions and notebooks for each chapter currently completed |
| `data/`                  | All utilized data |
| `apm_projects_env.yml`   | Conda environment definition file |
| `access_data.md`         | How to access datasets from R |
| `README.md`              | This file |

## Data Access

The file `access_data.md` provides an example of how to extract datasets directly from R, for those who wish to start from scratch rather than reuse the pre-converted Parquet files provided in the data folder.