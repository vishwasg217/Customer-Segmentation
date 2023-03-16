from setuptools import find_packages, setup


def get_requirements(path: str) -> list:
    requirements = []
    with open(path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements


setup(
    name='customer_segmentation',
    version='0.0.1',
    author='Vishwas Gowda',
    author_email='vishwas.g217@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
