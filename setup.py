import setuptools
from distutils.core import setup

setup(name='sade',
      version='1.0',
      description='Software Architecture with Document Embeddings',
      author='Marios Papachristou',
      author_email='papachristoumarios@gmail.com',
      url='https://github.com/papachristoumarios/sade',
      packages=['sade'],
      scripts=['sade/clustering.py', 'sade/embeddings.py', 'sade/corrcoef.py', 'sade/layerize.py', 'sade/community_detection.py']	
     )
