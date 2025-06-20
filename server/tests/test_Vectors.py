from utils.Testing import BaseTest, register_test_class, priority, TestPriority
from utils.types.Vectors import *


@register_test_class
class VectorOPTests(BaseTest):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.setUp()


#----------------------------------------------------------#

    @priority(TestPriority.UTILS)
    def test_vector_1d_add(self):
        v1 = Vector1d(5.0)
        v2 = Vector1d(5.0)
        
        self.assertEqual(Vector1d(10.0), v1.add(v2))

    @priority(TestPriority.UTILS)
    def test_vector_1d_sub(self):
        v1 = Vector1d(5.0)
        v2 = Vector1d(5.0)
        
        self.assertEqual(Vector1d(0.0), v1.subtract(v2))

    @priority(TestPriority.UTILS)
    def test_vector_1d_mul(self):
        v1 = Vector1d(5.0)
        v2 = Vector1d(5.0)
        
        self.assertEqual(Vector1d(25.0), v1.multiply(v2))

    @priority(TestPriority.UTILS)
    def test_vector_1d_div(self):
        v1 = Vector1d(5.0)
        v2 = Vector1d(5.0)
        
        self.assertEqual(Vector1d(1.0), v1.divide(v2))

#----------------------------------------------------------#

    @priority(TestPriority.UTILS)
    def test_vector_2d_add(self):
        v1 = Vector2d(5.0, 2.0)
        v2 = Vector2d(5.0, 2.0)
        
        self.assertEqual(Vector2d(10.0, 4.0), v1.add(v2))

    @priority(TestPriority.UTILS)
    def test_vector_2d_sub(self):
        v1 = Vector2d(5.0, 2.0)
        v2 = Vector2d(5.0, 2.0)
        
        self.assertEqual(Vector2d(0.0, 0.0), v1.subtract(v2))

    @priority(TestPriority.UTILS)
    def test_vector_2d_mul(self):
        v1 = Vector2d(5.0, 2.0)
        v2 = Vector2d(5.0, 2.0)
        
        self.assertEqual(Vector2d(25.0, 4.0), v1.multiply(v2))

    @priority(TestPriority.UTILS)
    def test_vector_2d_div(self):
        v1 = Vector2d(5.0, 2.0)
        v2 = Vector2d(5.0, 2.0)
        
        self.assertEqual(Vector2d(1.0, 1.0), v1.divide(v2))

#----------------------------------------------------------#

    @priority(TestPriority.UTILS)
    def test_vector_3d_add(self):
        v1 = Vector3d(5.0, 2.0, 10.0)
        v2 = Vector3d(5.0, 2.0, 10.0)
        
        self.assertEqual(Vector3d(10.0, 4.0, 20.0), v1.add(v2))

    @priority(TestPriority.UTILS)
    def test_vector_3d_sub(self):
        v1 = Vector3d(5.0, 2.0, 10.0)
        v2 = Vector3d(5.0, 2.0, 10.0)
        
        self.assertEqual(Vector3d(0.0, 0.0, 0.0), v1.subtract(v2))

    @priority(TestPriority.UTILS)
    def test_vector_3d_mul(self):
        v1 = Vector3d(5.0, 2.0, 10.0)
        v2 = Vector3d(5.0, 2.0, 10.0)
        
        self.assertEqual(Vector3d(25.0, 4.0, 100.0), v1.multiply(v2))

    @priority(TestPriority.UTILS)
    def test_vector_3d_div(self):
        v1 = Vector3d(5.0, 2.0, 10.0)
        v2 = Vector3d(5.0, 2.0, 10.0)
        
        self.assertEqual(Vector3d(1.0, 1.0, 1.0), v1.divide(v2))

#----------------------------------------------------------#

    @priority(TestPriority.UTILS)
    def test_vector_4d_add(self):
        v1 = Vector4d(5.0, 2.0, 10.0, 1.6)
        v2 = Vector4d(5.0, 2.0, 10.0, 1.6)
        
        self.assertEqual(Vector4d(10.0, 4.0, 20.0, 3.2), v1.add(v2))

    @priority(TestPriority.UTILS)
    def test_vector_4d_sub(self):
        v1 = Vector4d(5.0, 2.0, 10.0, 1.6)
        v2 = Vector4d(5.0, 2.0, 10.0, 1.6)
        
        self.assertEqual(Vector4d(0.0, 0.0, 0.0, 0.0), v1.subtract(v2))

    @priority(TestPriority.UTILS)
    def test_vector_4d_mul(self):
        v1 = Vector4d(5.0, 2.0, 10.0, 1.6)
        v2 = Vector4d(5.0, 2.0, 10.0, 1.6)
        
        self.assertEqual(Vector4d(25.0, 4.0, 100.0, 2.5600000000000005), v1.multiply(v2))

    @priority(TestPriority.UTILS)
    def test_vector_4d_div(self):
        v1 = Vector4d(5.0, 2.0, 10.0, 1.6)
        v2 = Vector4d(5.0, 2.0, 10.0, 1.6)
        
        self.assertEqual(Vector4d(1.0, 1.0, 1.0, 1.0), v1.divide(v2))