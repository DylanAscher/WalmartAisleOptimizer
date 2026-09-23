## WalmartAisleOptimizer
A Python script sorting and obtaining the aisle from given Walmart products.

## THE PROBLEM:
Walmart has no option to sort by aisle number, taking you from front to back. 
This changes that, allowing you to add your own items alongside using existing ones to optimize your Walmart trips.

## THE SETUP:
This script requires Python and relies on Conda for environments. If you don't have Conda, it's very useful for Python development. I recommend you get it.

**1. Create and activate the environment:**
```bash
conda create --name walmart-scraper python=3.10 -y
conda activate walmart-scraper
```

**2. Install the libraries:**
```bash
conda install pandas requests -y
pip install beautifulsoup4
```

**3. Run.**
```bash
python WalmartOptimizer.py
```

## THE STATUS:
Right now, this will only work for the Ames Walmart on Duff (#4265). I have updated the code as so. Future commits will try to remedy this.