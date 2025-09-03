# dslab-docai

# Pre Requisites

Install Virtualenv package:
```bash
pip install virtualenv
```

Create a virtual environment
```bash
python venv .venv
```

Activate the Virtual Environment,
following the specific instructions for your OS,
for example, with Win/Powershell: `.\.venv\Scripts\activate`


Install dependencies
```bash
pip install requirements.txt
```

Donwload `docling` models (if not automatically done):
```bash
docling-tools models download
```
The model artifacts are downloaded by default in `$HOME/.cache/docling/models`

This virtual environment has been built using Python 3.10.9 and Win11
There is a unresolved issue on Win OS [OSError: could not find or load spatialindex_c-64.dll](https://github.com/docling-project/docling/issues/867)
that may affect you.

As project is based in notebooks, three popular approaches can be followed:
* Install jupyter notebook: `pip install jupyter`
* Install jupyterlab: `pip install jupyterlab`
* Use VSCode notebooks extension: [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) 
and install ipykernel with `pip install ipykernel`


