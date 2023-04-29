# General Notes

To start a python container from a bash entry point
```
docker run -it --entrypoint=bash python:3.9
```

To build a container from a Dockerfile in the current working dir:
```
docker build -t test:pandas .
```

To run a container with arguments passed to the internal pipeline program:
```
docker run -it test:pandas <some_argument>
```

*Use double quotes with JSON(?) arrays in docker file*

Getting the first 100 rows of a CSV:
```
head -n 100 <file>
```

Count lines in a file (not sure if this works for CSV)
```
wc -l <file>
```

## Steps in loading