# --- Test Registry ---
from enum import Enum
import inspect
import io
import sys
from typing import Callable, Dict, List, Optional, Set
import unittest

import loguru

# --- Priority Enumeration and Decorator ---
class TestPriority(Enum):
    """Enumeration for test priorities."""
    CORE: int = 0
    UTILS: int = 1
    GAME: int = 2
    DATABASE: int = 3
    PERMISSION: int = 4
    PLAYER: int = 5
    PACKET: int = 6


def priority(value: TestPriority):
    """
    Decorator to assign a priority to a test method within a TestCase class.

    Args:
        value: The TestPriority value to assign.
    """
    def decorator(func):
        setattr(func, '_priority', value)
        return func
    return decorator

class TestRegistry:
    """Registry to hold and manage test classes."""
    _test_classes: Dict[type, List[tuple[str, Optional[TestPriority]]]] = {}  # Store test class and its methods with priorities

    @classmethod
    def register(cls, test_class: type):
        """Registers a test class and its test methods with their priorities."""
        if issubclass(test_class, BaseTest) and test_class not in cls._test_classes:
            test_methods_with_priority = []
            for name, method in inspect.getmembers(test_class, predicate=inspect.isfunction):
                if name.startswith('test_'):
                    priority_value = getattr(method, '_priority', test_class.priority if hasattr(test_class, 'priority') else None)
                    test_methods_with_priority.append((name, priority_value))
            cls._test_classes[test_class] = test_methods_with_priority
            loguru.logger.debug(f"Registered test class: {test_class.__name__} with methods and priorities.")

    @classmethod
    def get_tests_for_priority(cls, priorities: Optional[Set[TestPriority]] = None) -> unittest.TestSuite:
        """Returns a TestSuite containing tests filtered by the specified priorities."""
        suite = unittest.TestSuite()
        for test_class, methods_with_priority in cls._test_classes.items():
            for method_name, priority_value in methods_with_priority:
                if priorities is None or priority_value in priorities or (priority_value is None and TestPriority.CORE in priorities):
                    suite.addTest(test_class(methodName=method_name))
        return suite

    @classmethod
    def get_all_registered_classes(cls) -> List[type]:
        """Returns a list of all registered test classes."""
        return list(cls._test_classes.keys())


# --- Base Test Class ---
class BaseTest(unittest.TestCase):
    """
    Base class for creating test cases. Provides basic structure, result tracking, and loguru integration.
    Inherits from unittest.TestCase for standard testing functionality.
    """
    priority: Optional[TestPriority] = TestPriority.CORE  # Default class-level priority

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.results: Dict[Callable, Optional[bool]] = {}  # Store results of individual test methods (True: pass, False: fail, None: skip)
        self._test_methods: List[str] = []
        self._current_test_method: Optional[str] = None
        if not hasattr(self, '_is_setup'):
            self._is_setup = False

    def setUp(self):
        """Set up method executed before each test method."""
        super().setUp()
        self._test_methods = [method for method in dir(self) if method.startswith('test_')]
        self._sort_tests_by_priority()
        self._is_setup = True
        #loguru.logger.debug(f"Setting up test case: {self.__class__.__name__}")

    def tearDown(self):
        """Tear down method executed after each test method."""
        if self._current_test_method and self._is_setup:
            outcome = self.defaultTestResult()
            test_method = getattr(self, self._current_test_method)
            return_value = self._feedErrorsToResult(outcome, test_method, self, self._current_test_method)
            self.results[test_method] = not (outcome.failures or outcome.errors) if not outcome.skipped else None
            loguru.logger.debug(f"Finished test method: {self._current_test_method} in {self.__class__.__name__} - Return '{return_value}' - Result: {'PASSED' if self.results.get(test_method) is True else 'FAILED' if self.results.get(test_method) is False else 'SKIPPED'}")
            self._current_test_method = None
        super().tearDown()

    def _get_priority(self, method_name: str) -> Optional[TestPriority]:
        """
        Helper method to get the priority of a specific test method.
        Checks for the '_priority' attribute set by the @priority decorator.
        """
        method = getattr(self, method_name)
        return getattr(method, '_priority', getattr(self.__class__, 'priority', None))

    def _sort_tests_by_priority(self):
        """Sorts the test methods based on their priority (HIGH > MEDIUM > LOW)."""
        self._test_methods.sort(key=lambda method_name: (self._get_priority(method_name) or TestPriority.LOW).value, reverse=True)

    def _feedErrorsToResult(self, result, method, test, test_method_name):
        """A simplified version of unittest's _feedErrorsToResult, now capturing return value."""
        return_value = None
        try:
            return_value = method()  # Execute the test method and capture its return value
        except self.failureException as e:
            result.addFailure(test, sys.exc_info())
            self.results[method] = (False, None)
            #loguru.logger.error(f"Test '{test_method_name}' in {self.__class__.__name__} failed: {e}")
        except unittest.SkipTest as e:
            result.addSkip(test, str(e))
            self.results[method] = (None, None)  # Indicate skipped
            #loguru.logger.info(f"Test '{test_method_name}' in {self.__class__.__name__} skipped: {e}")
        except Exception as e:
            result.addError(test, sys.exc_info())
            self.results[method] = (False, None)
            #loguru.logger.error(f"Test '{test_method_name}' in {self.__class__.__name__} encountered an error: {e}")
        else:
            result.addSuccess(test)
            self.results[method] = (True, return_value)
            #loguru.logger.info(f"Test '{test_method_name}' in {self.__class__.__name__} passed.")
        return return_value

    def run(self, result=None):
        """Override the run method to set the current test method."""
        self._current_test_method = self.id().split('.')[-1]
        return super().run(result) # Call the standard run method



# --- Test Runner ---
def run_tests(priorities_to_run: Optional[Set[TestPriority]] = None, log_summary = False):
    """Discovers and runs test classes, optionally filtering by priority.

    Args:
        priorities_to_run: A set of TestPriority values to run. If None, all tests are run.
    """
    loguru.logger.info(f"Running Tests with priorities: {[x.name for x in priorities_to_run] if priorities_to_run else 'All'}...")
    suite = TestRegistry.get_tests_for_priority(priorities_to_run)

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=0)
    result = runner.run(suite)

    # Now iterate through the *result* object to get the aggregated counts
    total_passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total_failed = len(result.failures) + len(result.errors)
    total_skipped = len(result.skipped)

    if log_summary:
        loguru.logger.info(f"--- Test Summary (Filtered by: {[x.name for x in priorities_to_run] if priorities_to_run else 'All'} )---")
        loguru.logger.info(f"Total Tests Run: {result.testsRun}")
        loguru.logger.info(f"Total Passed: {total_passed}")
        loguru.logger.info(f"Total Failed: {total_failed}")
        loguru.logger.info(f"Total Errors: {len(result.errors)}")
        loguru.logger.info(f"Total Skipped: {total_skipped}")

    return result


# --- Test Registration Decorator ---
def register_test_class(cls):
    """Decorator to register a test class with the TestRegistry."""
    TestRegistry.register(cls)
    return cls