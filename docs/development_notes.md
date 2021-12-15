# Development notes
## About unit tests and F.I.R.S.T. principles
When developing the unit tests for the [v0.3 milestone](https://github.com/noise-kngdm/music-matcher/milestone/4), we followed these principles to develop quality unit tests.
### Fast
The **98** unit tests programmed for this milestone, which cover a great part of the business logic, run in a matter of `0.2` seconds on a mid-tier laptop. For example, we avoided making expensive calls to some  procedures by monkey-patching them, as in this example:
https://github.com/noise-kngdm/music-matcher/blob/338ee501ed2fec2ec9910b1694e4e2ee5b8c4e80/music_matcher/tests/test_recommendation_engine.py#L101-L105

### Isolated
We used fixtures to set up the testing data to ensure that the unit tests don't interfere with each other.

### Repeatable
The set of test data is defined in a deterministic way, from dates used to songs data, and is generated for each test. This way, all tests should have the same results when executed for the same code.

### Self-validating
Almost all tests use `assertpy` to determine if the test has failed or not in a natural language-friendly way, so the interpretation of the results is clear. The ones that don't use `assertpy` either check that a particular exception was raised or that a constructor was executed without raising any exceptions. All of the test names have an evident name that lets the tester know what failed with only reading the test's name.

### Timely
The unit tests were written while developing the business logic and test the edge values that could be given to the developed code. No part of the business logic is left without testing.
