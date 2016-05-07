# _*_ utf8 _*_


from setuptools import setup


setup(
    name="socket echo server",
    description="Utilizes sockets to create an echo server",
    version=0.1,
    author="Rick Tesmond and Wenjing Qiang",
    license="MIT",
    py_modules=["server", "client"],
    package_dir={"": "src"},
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-xdist', 'tex']},
)
