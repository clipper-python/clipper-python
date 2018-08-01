# Clipper-Python

Fully self-contained Python wrapping of Kevin Cowtan's [Clipper](http://www.ysbl.york.ac.uk/~cowtan/clipper/doc/) library for handling of crystallographic and cryo-EM macromolecular data. 

## Getting Started

(Note: the below assumes that 'python3' is your system Python executable. Substitute your own as necessary, but note that the installer is not yet compatible with Python 2.7)

Clone into a local directory, then run:

python3 bundle_builder.py wheel 

(Add the switch --parallel for faster compiling)

Then,

cd dist
python3 -m pip install --user ./Clipper_Python-0.2*.whl


### Prerequisites

```
- Python 3 or above, with a recent version of Numpy installed
- Pybind11 headers installed on the system search path.
```
**NOTE**: as per [this discussion](https://github.com/pybind/pybind11/issues/1317) on the pybind11 GitHub issues, you may need to edit `pybind11.h` to replace the line:

```
record.default_holder = std::is_same<holder_type, std::unique_ptr<type>>::value;
```

with 

```
record.default_holder = detail::is_instantiation<std::unique_ptr, holder_type>::value;
```



## License

This project is licensed under the LGPL v.3.0 License - see the [LICENSE.md](LICENSE.md) file for details


