import re
import os
import argparse
from datetime import datetime
from csv import DictWriter
from collections import Counter

from dotenv import load_dotenv
import praw

# Load auth info from .env file
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')

# Instantiate praw client
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# The following regex patterns look for each of the different fields of
# interest and have a group for the corresponding value
COMPANY_REGEX = re.compile(r'.*?Company.*?:(.+)$', re.IGNORECASE)
LOCATION_REGEX = re.compile(r'.*?Location.*?:(.+)$', re.IGNORECASE)
SALARY_REGEX = re.compile(r'.*?Salary.*?:(.+)$', re.IGNORECASE)
RELOCATION_REGEX = re.compile(r'.*?Relocation.*?:(.+)$', re.IGNORECASE)
SIGNING_REGEX = re.compile(r'.*?Signing.*?:(.+)$', re.IGNORECASE)
STOCK_REGEX = re.compile(r'.*?Stock.*?:(.+)$', re.IGNORECASE)
TOTAL_REGEX = re.compile(r'.*?Total.*?:(.+)$', re.IGNORECASE)


class Salary:
    """
    Salary contains the "values" associated with each of the fields commonly provided in the salary sharing thread.

    If no value could be found for a field, the property's value will be None.

    This object is "truthy" if both company and salary properties are not None. 
    This makes it easier to check whether this Salary entry contains useful information since these are the most important fields to know.
    """

    # List of field names that are parsed out of salary sharing comments
    FIELDNAMES = ['Date', 'Company', 'Salary', 'Location',
                  'Relocation', 'Signing', 'Stock', 'Total', 'Url']

    def __init__(self, submission, comment):
        self.company = None
        self.location = None
        self.salary = None
        self.relocation = None
        self.signing = None
        self.stock = None
        self.total = None
        self.comment = comment
        self.submission = submission
        self.parse_comment()

    def parse_comment(self):
        """
        Sets each of the properties of this Salary object if a corresponding value is found within the given comment

        It will only take the first instance of each field that it finds.
        i.e. in the following comment self.company would end up being A:
        Company: A
        Company: B
        """
        for line in self.comment.body.split(sep='\n'):
            if self.company is None:
                self.company = get_regex_group(COMPANY_REGEX, line)
            if self.location is None:
                self.location = get_regex_group(LOCATION_REGEX, line)
            if self.salary is None:
                self.salary = get_regex_group(SALARY_REGEX, line)
            if self.relocation is None:
                self.relocation = get_regex_group(RELOCATION_REGEX, line)
            if self.signing is None:
                self.signing = get_regex_group(SIGNING_REGEX, line)
            if self.stock is None:
                self.stock = get_regex_group(STOCK_REGEX, line)
            if self.total is None:
                self.total = get_regex_group(TOTAL_REGEX, line)

    def __str__(self):
        return 'Company: {}\nLocation: {}\nSalary: {}\nRelocation: {}\nSigning: {}\nStock: {}\nTotal: {}'.format(
            self.company, self.location, self.salary, self.relocation, self.signing, self.stock, self.total)

    def to_dict(self):
        """Returns a dictionary containg each of the Salary properties along with its corresponding value"""
        d = {}
        d['Company'] = self.company if self.company else ""
        d['Location'] = self.location if self.location else ""
        d['Salary'] = self.salary if self.salary else ""
        d['Relocation'] = self.relocation if self.relocation else ""
        d['Signing'] = self.signing if self.signing else ""
        d['Stock'] = self.stock if self.stock else ""
        d['Total'] = self.total if self.total else ""
        d['Date'] = datetime.utcfromtimestamp(self.comment.created_utc)
        d['Url'] = self.to_url()
        return d

    def to_url(self):
        """Returns the url of the associated comment as a string."""
        return '{}{}'.format(self.submission.url, self.comment.id)

    def __bool__(self):
        # This should be "truthy" if it has both a company and salary defined
        return (self.salary is not None) and (self.company is not None)


def get_regex_group(pattern, string):
    res = pattern.match(string)
    if not res:
        return None
    return res.group(1).strip()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Retrieve offer information from /r/cscareerquestions salary sharing threads and output them to a csv.')
    parser.add_argument('--output', type=argparse.FileType('w'),
                        default='output/salaries.csv', help='File to save csv output to.')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='If true, prints salary info to the screen as they are parsed.')
    return parser.parse_args()


def main():
    args = parse_args()
    # The ids of the salary sharing posts. Manually retrieved, but could possible be automated in the future.
    submission_ids = ['czhew5', 'bwzppv', 'a39y3m', 'axw08t', '9d3zy4',
                      '8oyl4o', '6ye3fs', '82merx', '7hwf8c', '5h6xvj', '6grx7f']
    salaries = []
    num_total_comments = 0
    num_salary_comment = 0
    location_counter = Counter()
    company_counter = Counter()
    for id in submission_ids:
        submission = reddit.submission(id=id)
        for comment in submission.comments.list():
            num_total_comments += 1
            if isinstance(comment, praw.models.MoreComments):
                # Occasionally MoreComments instances will appear even though the .list() method was used
                continue
            s = Salary(submission, comment)
            if s:
                num_salary_comment += 1
                location_counter[s.location] += 1
                company_counter[s.company] += 1
                salaries.append(s)
                if args.verbose:
                    print(s)
                    print('========================================================')
    writer = DictWriter(args.output, fieldnames=Salary.FIELDNAMES)
    writer.writeheader()
    for s in salaries:
        writer.writerow(s.to_dict())
    print('{} Salaries Recorded From {} Relevant Comments (Out Of {} Total) In {} Salary Sharing Threads'.format(len(salaries), num_salary_comment, num_total_comments, len(submission_ids)))
    if args.verbose:
        print('{:.1f}% of comments were salaries\n'.format(100 * num_salary_comment / num_total_comments))
        print('10 Most Common Companies:')
        for company, count in company_counter.most_common(10):
            print('\t{}: {}'.format(company, count))
        print('\n10 Most Common Locations:')
        for location, count in location_counter.most_common(10):
            print('\t{}: {}'.format(location, count))


if __name__ == '__main__':
    main()
