## Gmail Takeout Curve emails to CSV

This tool reads MBOX files from [Google Takout](https://takeout.google.com/settings/takeout), parses [Curve](https://www.curve.app/en/join#ZEJZ226D) (<- contains referral code) transaction emails and outputs CSV files which then can be imported to budget tracking apps, like [Lunch Money](https://lunchmoney.cc/).

## Usage

The app takes a single parameter which is a path to an MBOX file containing all the emails.

    python convert.py --input receipts.mbox

Parsed transactions will be grouped by month and placed to the `target/` directory.
Any unparsed emails will be saved under the `target/` directory with a `unparsed-` prefix.  
