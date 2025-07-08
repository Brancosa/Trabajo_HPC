from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "simulacion",
        ["simulacion.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=["-O3", "-std=c++11"],
    ),
]

setup(
    name="simulacion",
    ext_modules=ext_modules,
)
