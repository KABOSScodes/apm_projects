# README – Applied Predictive Modeling Projects

This repository contains solutions and explorations based on *Applied Predictive Modeling* by Max Kuhn and Kjell Johnson. The original book uses R, but all work here is implemented in Python.

This is **not** a strict line-by-line translation of the R code. Many projects include extended analysis, helper functions, and visualizations that go beyond the original book—either because they were good learning opportunities or personally interesting to investigate.

## Table of Contents

- [Purpose](#purpose)
- [Environment Setup](#environment-setup)
- [Repository Structure](#repository-structure)
- [Brief Project Descriptions](#brief-project-descriptions)
- [Data Access](#data-access)
- [Reproducibility Notes](#reproducibility-notes)

## Purpose

The goal of this project is to deepen my understanding of predictive modeling techniques by reproducing and expanding on the exercises from *Applied Predictive Modeling* using Python.

## Environment Setup

The repository uses a Conda environment defined in `APMProjects_env.yml`. To recreate it:

```bash
conda env create -f APMProjects_env.yml
conda activate APMProjects
```
## Repository Structure

| Folder/File              | Description |
|--------------------------|-------------|
| `Pre-Processing/`        | Scripts and notebooks for data cleaning and transformation |
| `Project1/`              | First applied modeling project (e.g., segmentation tasks) |
| `RChapterScripts/`       | Original R code from the book, included for reference |
| `APMProjects_env.yml`    | Conda environment definition file |
| `AccessData.md`          | How to access datasets from R |
| `plots.ipynb`            | Experiments and standalone visualizations |
| `bash_commands.md`       | Notes on useful shell commands |
| `todo.txt`               | Personal task list |
| `README.md`              | This file |


## Brief Project descriptions

## Data Access

The file `AccessData.md` provides an example of how to extract datasets directly from R, for those who wish to start from scratch rather than reuse the pre-converted Parquet files provided in each project folder.

## Reproducibility Notes
Paths: Some scripts may contain hardcoded paths. To avoid issues, it’s recommended to clone this repository directly to your Desktop, or adjust paths as needed.

Data: If you prefer not to pull the data from R yourself, each project folder contains the necessary Parquet-formatted datasets.

## Test Area

1) test
2) another test
    * a
    * b
    * c
3) That was it

* Hmm
* Hi

1. Numbering again
2. Still...

