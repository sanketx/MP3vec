from setuptools import setup

setup(

    name="mp3vec",
    version='1.0.0',
    description="A Transferable Feature Representation Method for Protein Sequences",
    url="https://github.com/sanketx/MP3vec",
    author="Sanket Rajan Gupte",
    author_email="sanketgupte14@gmail.com",
    packages=["mp3vec"],
    install_requires=[
        "tensorflow==2.9.3",
        "biopython==1.72"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mp3vec=mp3vec.vectorize_directory:vectorize_directory",
            "mp3pssm=mp3vec.make_pssm:make_pssm"
        ]
    },
    zip_safe=False,
)
