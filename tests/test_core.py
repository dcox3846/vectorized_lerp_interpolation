import unittest

from vectorized_lerp_interpolation import lerp, lerp_array, lerp_segment


class TestLerpScalar(unittest.TestCase):
    def test_basic_midpoint(self):
        self.assertAlmostEqual(lerp(0.0, 10.0, 0.5), 5.0)

    def test_endpoints(self):
        self.assertAlmostEqual(lerp(2.0, 8.0, 0.0), 2.0)
        self.assertAlmostEqual(lerp(2.0, 8.0, 1.0), 8.0)

    def test_clamp_low(self):
        self.assertAlmostEqual(lerp(0.0, 10.0, -1.0), 0.0)

    def test_clamp_high(self):
        self.assertAlmostEqual(lerp(0.0, 10.0, 2.0), 10.0)

    def test_extrapolate_low(self):
        self.assertAlmostEqual(lerp(0.0, 10.0, -1.0, clamp=False), -10.0)

    def test_extrapolate_high(self):
        self.assertAlmostEqual(lerp(0.0, 10.0, 2.0, clamp=False), 20.0)

    def test_int_inputs_return_float(self):
        result = lerp(1, 3, 0.5)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 2.0)


class TestLerpArray(unittest.TestCase):
    def test_matching_lengths_scalar_t(self):
        got = lerp_array([0.0, 1.0, 2.0], [10.0, 11.0, 12.0], 0.5)
        self.assertEqual(got, [5.0, 6.0, 7.0])

    def test_matching_lengths_sequence_t(self):
        got = lerp_array([0.0, 0.0], [10.0, 20.0], [0.25, 0.75])
        self.assertAlmostEqual(got[0], 2.5)
        self.assertAlmostEqual(got[1], 15.0)

    def test_clamp_applies_per_element(self):
        got = lerp_array([0.0, 0.0], [10.0, 10.0], [-1.0, 2.0])
        self.assertEqual(got, [0.0, 10.0])

    def test_extrapolate_per_element(self):
        got = lerp_array([0.0, 0.0], [10.0, 10.0], [-1.0, 2.0], clamp=False)
        self.assertEqual(got, [-10.0, 20.0])

    def test_length_mismatch_a_b(self):
        with self.assertRaises(ValueError):
            lerp_array([0.0, 1.0], [10.0], 0.5)

    def test_length_mismatch_t(self):
        with self.assertRaises(ValueError):
            lerp_array([0.0, 1.0], [10.0, 11.0], [0.5])

    def test_empty_arrays(self):
        self.assertEqual(lerp_array([], [], 0.5), [])


class TestLerpSegment(unittest.TestCase):
    def test_scalar_points_scalar_t(self):
        got = lerp_segment(0.0, 10.0, 0.5)
        self.assertAlmostEqual(got, 5.0)

    def test_sequence_points_scalar_t(self):
        got = lerp_segment([0.0, 0.0], [10.0, 20.0], 0.5)
        self.assertEqual(got, [5.0, 10.0])

    def test_scalar_points_sequence_t(self):
        got = lerp_segment(0.0, 10.0, [0.0, 0.5, 1.0])
        self.assertEqual(got, [0.0, 5.0, 10.0])

    def test_sequence_points_sequence_t(self):
        got = lerp_segment([0.0, 0.0], [10.0, 20.0], [0.0, 1.0])
        self.assertEqual(got, [[0.0, 0.0], [10.0, 20.0]])

    def test_steps_generates_even_samples(self):
        got = lerp_segment(0.0, 10.0, 0.0, steps=3)
        self.assertEqual(got, [0.0, 5.0, 10.0])

    def test_steps_with_sequence_points(self):
        got = lerp_segment([0.0, 0.0], [10.0, 20.0], 0.0, steps=2)
        self.assertEqual(got, [[0.0, 0.0], [10.0, 20.0]])

    def test_steps_less_than_one_raises(self):
        with self.assertRaises(ValueError):
            lerp_segment(0.0, 10.0, 0.5, steps=0)

    def test_mixed_point_types_raise(self):
        with self.assertRaises(TypeError):
            lerp_segment(0.0, [10.0, 20.0], 0.5)

    def test_clamp_false_extrapolates(self):
        got = lerp_segment(0.0, 10.0, 2.0, clamp=False)
        self.assertAlmostEqual(got, 20.0)

    def test_clamp_true_clamps(self):
        got = lerp_segment(0.0, 10.0, 2.0, clamp=True)
        self.assertAlmostEqual(got, 10.0)


if __name__ == "__main__":
    unittest.main()
