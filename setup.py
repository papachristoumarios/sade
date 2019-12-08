"""Setup module"""
from setuptools import setup

setup(
    name='sade',
    version='1.0',
    description='Software Architecture with Document Embeddings',
    author='Marios Papachristou',
    author_email='papachristoumarios@gmail.com',
    url='https://github.com/papachristoumarios/sade',
    packages=[
        'sade',
        'sade.mojo',
        'sade.limbo'],
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
        'sade/limbo.py',
        'sade/layerize.py',
        'sade/community_detection.py',
        'sade/autogen_module.py',
        'sade/json_join.py',
        'sade/call_graph_analysis.py',
        'sade/simple_community_detection.py',
        'sade/bow.py',
        'sade/visualize_graphs.py',
        'sade/visualize_radar.py'])
