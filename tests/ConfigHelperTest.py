from src.utils.config_utils import ConfigHelper

class ConfigHelperTest:
    @staticmethod
    def test_get_root_dir():
        # should contain src, tests directories and pyproject.toml file
        config_helper = ConfigHelper()
        root_dir = config_helper.get_root_dir()

        assert root_dir is not None, "Root directory should not be None"
        assert root_dir.exists(), "Root directory should exist"
        assert (root_dir / "src").exists(), "Src directory should exist"
        assert (root_dir / "tests").exists(), "Tests directory should exist"
        assert (root_dir / "pyproject.toml").exists(), "Pyproject.toml file should exist"

if __name__ == "__main__":
    test_methods = {
        "test_get_root_dir": ConfigHelperTest.test_get_root_dir
    }

    print("Running ConfigHelper tests...\n")

    for test_name, test in test_methods.items():
        print(f"Running {test.__name__}...")
        test()
        print(f"{test.__name__} passed.\n")