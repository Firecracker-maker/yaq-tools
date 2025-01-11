# Yaq Tool

----------------
# Table of Contents

- [Welcome to yaq-tools](#welcome-to-yaq-tools)
- [Intuitive Python Pacakge](#intuitive-python-package)
- [Normalizing a Time Series of Data](#normalizing-a-time-series-of-data)
- [Cheatsheet](#cheatsheet)

# Welcome to yaq-tools
Over the years, as I’ve explored my voice and interests, I’ve found myself repeatedly drawn to the fascinating challenges of the data world. Data has a unique ability to teach us—its patterns, anomalies, and complexities often reveal unexpected insights. My passion lies in understanding these challenges and embracing the learning process that comes with them.

Recently, I began documenting my journey through a blog, sharing hands-on experiences in data management, 
financial insights, and career growth. Check-out my Quant Chronicle section [here](https://womenunbound.substack.com/s/quant-chronicles)

This repository, yaq-tools, serves as a safe space for me to share my thought processes. 
While technologies evolve, I believe what truly stands the test of time is our ability to deeply understand problems and approach them with clarity and curiosity. 
Here, you’ll find the reflections and approaches I’ve developed while tackling various data challenges.

Thank you for joining me on this journey—let’s explore and grow together!

# Intuitive Python Package
In this script, I aim to verify whether my Python package was created as intended.
In the field of Data Analytics, one of the most widely used Python packages is pandas—arguably the most essential. 
I've always been impressed by how user-friendly this package is. 
I believe its intuitive API design and consistent naming conventions are key factors behind the library's success 
and effectiveness.

Check out the `yaqtools/__init__` file to understand how we can simplify your imports.


# Normalizing a Time Series of Data
## Problem statement
Financial data has been a cornerstone of decision-making for decades. 
As technology evolves, platforms must adapt to handle the growing complexity and 
volume of data. Organizations face significant challenges in migrating, patching and 
transforming data to align with new platforms, 
which often requires extensive effort to ensure compatibility, consistency, and quality.

We aim to build a system that efficiently processes, transforms, and manipulates files 
to ensure seamless compatibility with evolving technologies.

## Features
Here are series of problem you may face when building and normalizing a Time Series of Data


## Techonology used
- Python
- Pandas
- DeltaLake - My [Quant Chronicle](https://womenunbound.substack.com/p/quant-chronicles-deltalakea-powerful) talks about it


# CheatSheet
*setup you venv*
``
conda create -n yaqtools python=3.11 -y
``

*activate*
``
conda activate yaqtools
``

*pip install via setup.py*
``
pip install -e '.[all]' 
``
