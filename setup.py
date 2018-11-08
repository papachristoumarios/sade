import setuptools
from setuptools import setup, find_packages

setup(
    name='sade',
    version='1.0',
    description='Software Architecture with Document Embeddings',
    author='Marios Papachristou',
    author_email='papachristoumarios@gmail.com',
    url='https://github.com/papachristoumarios/sade',
    packages=[
        'sade',
        'sade.mojo'],
    package_dir={
        'sade': 'sade',
        'sade.mojo': 'sade/mojo'},
    package_data={
        'sade.mojo': ['sade/mojo/*.java']},
    include_package_data=True,
    scripts=[
        'sade/clustering.py',
        'sade/embeddings.py',
        'sade/corrcoef.py',
        'sade/layerize.py',
        'sade/community_detection.py',
        'sade/autogen_module.py',
        'sade/json_join.py',
        'sade/call_graph_analysis.py'])
