from setuptools import setup, find_packages

setup(name='pymonads',
        version='0.1',
        description='Well typed functional programming abstactions in Python',
        url='http://github.com/amackillop/pymonads',
        author='Austin Mackillop',
        author_email='austin.mackillop@gmail.com',
        license='MIT',
        package_dir={'': 'src'},
        packages=find_packages('src'),
        zip_safe=True)
