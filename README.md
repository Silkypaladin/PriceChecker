# PriceChecker
Simple web scraping app, created to get, group and analyze items from a category given by the user. It works for products available on [x-kom](https://www.x-kom.pl)

## Prerequisites

The script uses two external libraries: **Selenium** and **Pandas**.
To install them, type in two commands given below.
```bash
pip install selenium
```
```bash
pip install pandas
```
The script uses Chrome version 83. Please, verify the version to stop any potential bugs.
## Running the script
If you want to run the script from the command line, simply type:
```bash
python3 scraper.py
```
When in project folder.
The program will first ask you to give a name of an item and provide price range. Next, it will perform the search and the analysis. You can export the results to **.csv** file by typing *yes* after the correct prompt.
If you want to run chrome in headless mode, uncomment the line:
```python
def  perform_search():
	...
	#opt.set_headless_mode(options)
	...
```

## Issues
It's a simple project made to have some fun. If you find any issues though, feel free to report them.
