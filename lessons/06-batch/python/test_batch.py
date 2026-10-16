import unittest

from batch import Job, Material, grams_by_material, heaviest_job, jobs_using, total_grams


def friday_queue() -> list[Job]:
    return [
        Job("benchy", Material.PLA, 12.5),
        Job("bracket", Material.PETG, 40.0),
        Job("phone case", Material.TPU, 22.25),
        Job("vase", Material.PLA, 85.0),
        Job("enclosure hinge", Material.ABS, 7.75),
    ]


class BatchTest(unittest.TestCase):
    def test_total_grams_of_a_batch(self):
        self.assertEqual(167.5, total_grams(friday_queue()))

    def test_total_grams_of_no_jobs_is_zero(self):
        self.assertEqual(0, total_grams([]))

    def test_grams_by_material(self):
        self.assertEqual(
            {Material.PLA: 97.5, Material.PETG: 40.0, Material.TPU: 22.25, Material.ABS: 7.75},
            grams_by_material(friday_queue()),
        )

    def test_grams_by_material_leaves_out_materials_that_are_not_used(self):
        jobs = [Job("benchy", Material.PLA, 12.5)]
        self.assertEqual({Material.PLA: 12.5}, grams_by_material(jobs))

    def test_jobs_using_pla_in_order(self):
        self.assertEqual(["benchy", "vase"], jobs_using(friday_queue(), Material.PLA))

    def test_jobs_using_a_material_nobody_uses(self):
        jobs = [Job("benchy", Material.PLA, 12.5)]
        self.assertEqual([], jobs_using(jobs, Material.ABS))


class HeaviestJobTest(unittest.TestCase):
    """One example. Write the tricky cases before the code."""

    def test_the_heaviest_job_in_the_batch(self):
        job = heaviest_job(friday_queue())
        self.assertIsNotNone(job)
        assert job is not None  # tells the type checker too
        self.assertEqual("vase", job.name)

    def test_no_jobs_means_no_heaviest_job(self):
        self.assertIsNone(heaviest_job([]))

    def test_the_first_of_two_equally_heavy_jobs_wins(self):
        jobs = [
            Job("left bracket", Material.PETG, 40.0),
            Job("right bracket", Material.PETG, 40.0),
        ]
        job = heaviest_job(jobs)
        assert job is not None
        self.assertEqual("left bracket", job.name)


if __name__ == "__main__":
    unittest.main()
