from setuptools import setup, find_packages

setup(
    name='colab_text_analyzer',
    version='0.1',
    packages=find_packages(),
    author='Jaime Polanco-Jimenez',
    author_email='jaime.polanco@javeriana.edu.co',
    description='A package to chat with multiples pdf  in Google Colab',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/polanco-jaime/colab_text_analyzer',
    install_requires=[
        'google-generativeai',
        'langchain-google-genai',
        'python-dotenv',
        'langchain',
        'pypdf',
        'chromadb'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

