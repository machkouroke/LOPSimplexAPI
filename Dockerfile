FROM abelsiqueira/python-and-julia:py3.10-jl1.6


COPY block.py .
CMD python block.py