# WikiSearch
A Python script that gets entries from txt file and search for it in Wikipedia

### Get it work!


#### 0. Install Python, requests and BeautifulSoup 
WikiSearch scraps the Wikipedia webcode to get requested info so you must install them:
[`Python`](https://www.python.org/downloads/ "Python")[`requests`](https://2.python-requests.org/en/master/user/install/#install "requests")[`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
In *Linux* simply type:

    sudo apt install Python3
    pip install requests BeautifulSoup4
    
#### 1. Launch it 
Open terminal and type 

    python3 <WikiSearch.py location> <your txt file location> <.countryCodes> <options>
	
> Remember that python3 and WikiSearch.py location must be on first and second position

##### Examples
    python3 WikiSearch.py file.txt .pl .en -v -e
	python3 home/WikiSearch.py folder/file.txt
	
##### Txt file
This file should contain requested entries, each on a different line. Like this:

     Robert Lewandowski
	 August
	 wiki
Output will be written in this file:

    Robert Lewandowski
	Robert Lewandowski (Polish pronunciation: [ˈrɔbɛrt lɛvanˈdɔfskʲi] (listen); born 21 August 1988) is a Polish professional footballer who plays as a striker for Bayern Munich and is the captain o 	the Poland national team. He is renowned for his positioning, technique and finishing, and is 	widely regarded as one of the best strikers of his generation.
	https://en.wikipedia.org/w/index.php?search=Robert_Lewandowski
	August
	August is the eighth month of the year in the Julian and Gregorian calendars, and the fifth of 		seven months to have a length of 31 days. It was originally named Sextilis in Latin because it 		was the sixth month in the original ten-month Roman calendar under Romulus in 753 BC, with 	March being the first month of the year. About 700 BC, it became the eighth month when 				January and February were added to the year before March by King Numa Pompilius, who also gave it 29 days. Julius Caesar added two days when he created the Julian calendar in 46 BC (708 AUC), giving it its modern length of 31 days. In 8 BC, it was renamed in honor of Augustus. According to a Senatus consultum quoted by Macrobius, he chose this month because it was the time of several of his great triumphs, including the conquest of Egypt.
	https://en.wikipedia.org/w/index.php?search=August
	wiki
	A wiki (/ˈwɪki/ (listen) WIK-ee) is a knowledge base website on which users collaboratively modify and structure content directly from the web browser. In a typical wiki, text is written using a simplified markup language and often edited with the help of a rich-text editor.
	https://en.wikipedia.org/w/index.php?search=wiki
	
##### Country codes
Those are Wikipedia's codes for county site like `pl` `en` or `pt`
If you give more than one country code the script will look for results for first code, if it won't find any it will look for second code etc.
##### Options
- `v` for output in terminal for every entry
- `e` for extended description in output txt file

You can put more than one option in a `-`. `-v -e` and `-ve` are equal 
