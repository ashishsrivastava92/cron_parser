Cron Expression Parser

  **Setup & Requirements**
- Python 3.7 <Install python - https://www.python.org/downloads/>
- pip install -r requirements.txt

**Run**
- python driver.py

**CLI Inputs**

- Help
- N
  - Add new cron string of format <|Cron Schedule| |Command> Example: */15 0 1,15 * 1-5 /usr/bin/find
  - Returns flattened object of schedule and command 
- S
  - Show all the cron-schedule + command added till now.


**Run Test Cases**
- Cron
  - python -m unittest tests.tests_cron_invalid.CronTestInvalid
  - python -m unittest tests.tests_cron.CronTest
- Segment
  - python -m unittest tests.tests_segments.SegmentTest

