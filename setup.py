from setuptools import setup, find_packages

setup(
    name='model_averaging_tool',
    version='0.1.0',
    description='A Python library for model averaging, data processing, and visualization.',
    author='Your Name',
    author_email='charles.shaw@tandpgroup.com.com',
    url='https://github.com/FixedPointIO/model_averaging_tool',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas==1.3.3',
        'numpy==1.21.2',
        'matplotlib==3.4.3',
        'seaborn==0.11.2',
        'scikit-learn==0.24.2',
        'prettytable==2.2.0',
        'jupyter==1.0.0',
        'notebook==6.4.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    python_requires='>=3.7',
)
