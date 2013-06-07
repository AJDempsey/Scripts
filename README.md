Scripts
=======

Scripts directory to make things easier


Todo the git diff input properly do the following


diff_var=`git diff`
./git_diff_parser.py "`echo -e \"$diff_var\"`"

This should be added to your git_precommit_hook folder some where and the out put used to run your unit tests.
