from setuptools import setup, find_packages

setup(name='pymonads',
      version='0.1.4',
      description='Well typed functional programming abstactions in Python',
      url='http://github.com/amackillop/pymonads',
      author='Austin Mackillop',
      author_email='austin.mackillop@gmail.com',
      license='MIT',
      packages=find_packages(exclude=('tests', 'docs')),
      package_data={
            'pymonads': ['py.typed']
      },
      zip_safe=False)
