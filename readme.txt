How to run the project?

1. Install virtual environment. Say virtual environment is installed under following directory:
/home/user/env

2. Now in the env folder, copy the top level source code folder - 'fuber'.

3. Now issue the command: cd /home/user/env/fuber

4. Now you can run all test cases by the following command:
	../bin/python -m unittest discover

5. A particular testcase can be run like following:
	../bin/python -m unittest test.test_trips.TripsTest.test_trip_order_amount