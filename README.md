# Yaq Tool

----------------
# Table of Contents

- [Welcome to yaq-tools](#welcome-to-yaq-tools)
- [Intuitive Python Pacakge](#intuitive-python-package)
- [Quality Controls](#quality-controls)
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

# Quality Controls

For decades, financial data has been a critical foundation for decision-making. As technology advances, platforms must evolve to manage the increasing complexity and volume of data. Organizations face significant challenges when migrating, patching, and transforming data to align with modern platforms, often requiring substantial effort to ensure compatibility, consistency, and quality.

My goal is to develop a system that efficiently processes, transforms, manipulates and quality control files to ensure seamless integration with emerging technologies.

To see an example in action, check out the scripts/demo_normalizing_data file, which demonstrates how robust data lakes can be built.

Note: This is an early prototype intended to spark discussion. It currently lacks several key features, including:
- Smart appending capabilities in Delta Lake
- Iteration over date ranges
- Support for step sequences defined in a configuration file (e.g., YAML)
- And much more.


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