from setuptools import setup

setup(name='geodict',
      version='0.1',
      description='A simple Python library/tool for pulling location information from unstructured text',
	  classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: GIS',
      ],
      url='https://github.com/petewarden/geodict',
      author='Pete Warden',
      author_email='pete@petewarden.com',
      license='GPL',
      packages=['geodict'],
	  install_requires=[
          'mysqlclient',
      ],
      zip_safe=False)