# /r/cscareerquestions Salary Scraper
The [/r/cscareerquestions](https://reddit.com/r/cscareerquestions) subreddit hosts periodic salary sharing threads where people share details of their job offers ([like this one](https://www.reddit.com/r/cscareerquestions/comments/czhew5/official_salary_sharing_thread_for_new_grads)). 

This script scrapes these threads for offer information and writes these details to a csv file. Currently it records info for the following fields: company, location, salary, relocation bonus, signing bonus, stock, and total compensation.

If you don't care about running the script and just want the data, then look at [output/salaries.csv](https://github.com/anders617/cscareerquestions-salaries/blob/master/output/salaries.csv)

## Setup
Clone this repository:
```shell
git clone https://github.com/anders617/cscareerquestions-salaries.git
```
Install the [praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html) Reddit API wrapper:
```shell
pip install praw
```
```shell
conda install -c conda-forge praw
```
Install the [dotenv](https://github.com/theskumar/python-dotenv) library:
```shell
pip install -U python-dotenv
```
```shell
conda install -c conda-forge python-dotenv
```
Next you will need to get credentials to make use of the Reddit API

Navigate to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) and click the "create app" button. You should create an app in order to get a client id and client secret.

Create a new .env file in the same directory as salaries.py with the following contents (using your new client id/secret):
```shell
CLIENT_ID='YOUR_CLIENT_ID'
CLIENT_SECRET='YOUR_CLIENT_SECRET'
USER_AGENT='python'

```

Run salaries.py in the terminal:
```shell
python salaries.py --output=output/salaries.csv --verbose
```

You should get output similar to the following:
```
[...]
========================================================
Company: Financial Institution
Location: Charlotte, NC
Salary: 70k
Relocation: None
Signing: None
Stock: 5 - 10%
Total: 77k
========================================================
Company: Health Insurance
Location: Buffalo, NY
Salary: $45,00 (That was a year ago, offer is now $50k)
Relocation: $0
Signing: $0
Stock: $2,300, but since we are a non-profit, bonuses are dependent on meeting our financial goals for the year.
Total: $53,000
========================================================
Company: Northrop Grumman
Location: Richmond VA
Salary: 52.5K
Relocation: None
Signing: None
Stock: I think we get these, a couple thousand if we hit goals.
Total: None
========================================================
Company: Digital Agency
Location: Southern Brazil
Salary: $5.9k (year)
Relocation: None
Signing: None
Stock: None
Total: None
========================================================
Company: SAAS
Location: Chicago
Salary: $75,000
Relocation: $0
Signing: $0
Stock: No stock, yearly bonus depends. My last one was about 1.6k
Total: None
========================================================
718 Salaries Recorded From 718 Relevant Comments (Out Of 4458 Total) In 11 Salary Sharing Threads
16.1% of comments were salaries

10 Most Common Companies:
        Google: 30
        Amazon: 24
        Microsoft: 20
        Big 4: 19
        Finance: 18
        Facebook: 15
        Defense: 10
        IBM: 10
        Capital One: 10
        Fintech: 7

10 Most Common Locations:
        Seattle: 33
        NYC: 27
        Bay Area: 25
        San Francisco: 16
        Chicago: 16
        London: 14
        Toronto: 13
        Redmond, WA: 12
        SF: 12
        Austin, TX: 12
```

Here are the first few lines of output/salaries.csv:

| Date                                                        | Company                                                                                                               | Salary                                                                                                          | Location     | Relocation                                                | Signing                                                                                                         | Stock                       | Total                                                           | Url                                                                                                             | 
|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|--------------|-----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------| 
|2019-09-09 20:38:39|**Amazon Web Services**|112k/yr|Austin Texas|9k lump sum post tax, miles/meals reimbursed|38k first year 22k second year|80k over 4 years|\~150k a year? plus|https://www.reddit.com/r/cscareerquestions/comments/czhew5/official_salary_sharing_thread_for_new_grads/ezqn8rr|
|2019-09-05 06:19:35|mature NYC startup|$105,000|New York|0|0|17,000 stock options|$105,000 (valuing options at $0)|https://www.reddit.com/r/cscareerquestions/comments/czhew5/official_salary_sharing_thread_for_new_grads/ez3bre4|
|2019-09-04 13:38:07|Finance|80k|Boston|5k|5k|0|85k|https://www.reddit.com/r/cscareerquestions/comments/czhew5/official_salary_sharing_thread_for_new_grads/eyyx82q|

You can view the entire output from a recent run in [output/salaries.csv](https://github.com/anders617/cscareerquestions-salaries/blob/master/output/salaries.csv)
