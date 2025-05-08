from utils.Testing import BaseTest, register_test_class, priority, TestPriority
from utils.Vectors import *


@register_test_class
class TemplateTests(BaseTest):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.setUp()


#----------------------------------------------------------#

    @priority(TestPriority.CORE)
    def test_function(self):
        self.assertEqual(True, True)