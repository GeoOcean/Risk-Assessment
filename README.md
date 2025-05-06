# Risk management of Natural Disasters
GeoOcean Engineering Group - Departamento de Ciencias y Técnicas del Agua y del Medioambiente
Universidad de Cantabria

## Install

The source code is currently hosted on GitLab at [this link](https://gitlab.com/geoocean/courses/risk)

## Folders

### Environment installation

Both environment and requirements can be installed navigating to the base root of [risk](./) and typing:

```
    # type in terminal
    conda env create -f environment.yml 
```

Manually installation of Cartopy:
```
    conda install -c conda-forge cartopy
```

## Launch Jupyter Lab

Activate the environment and launch jupyter lab:

```
    # type in terminal
    conda activate risk
    jupyter lab
```

## Main contents
Risk Assessment of Coastal Flooding in Apia, capital of Samoa [](./Coastal_flooding)

- [data](./Coastal_flooding/data/)
- [notebooks](./Coastal_flooding/notebooks/)
- [storage](./Coastal_flooding/storage/)

Risk Assessment of Rainfall Flooding in the Vasigano river basin, Samoa [](./Rainfall_flooding)

- [data](./Rainfall_flooding/data/)
- [notebooks](./Rainfall_flooding/notebooks/)
- [storage](./Rainfall_flooding/storage/)

## Prerequisites

Download the lastest stable version of RiskScape [clicking here](https://riskscape.org.nz/docs/intro/downloads.html#downloads)
RiskScape requires a Java Runtime Environment of at least version 8 to run.


## License

This project is licensed under the MIT License - see the [license](./LICENSE.txt) file for more details
