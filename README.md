[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# Mixed-Integer Programming Versus Constraint Programming for Shop Scheduling Problems: New Results and Outlook

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[This is a Template](https://doi.org/10.1287/ijoc.2019.0934) by Bahman Naderi, Rubén Ruiz, Vahid Roshanaei. 
The snapshot is based on 
[this SHA](https://github.com/tkralphs/JoCTemplate/commit/f7f30c63adbcb0811e5a133e1def696b74f3ba15) 
in the development repository. 

**Important: This code is being developed on an on-going basis at 
https://github.com/tkralphs/JoCTemplate. Please go there if you would like to
get a more recent version or would like support**

## Cite

To cite this software, please cite the [paper](https://doi.org/10.1287/ijoc.2019.0934) using its DOI and the software itself, using the following DOI.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7541223.svg)](https://doi.org/10.5281/zenodo.7541223)

Below is the BibTex for citing this version of the code.

```
@article{Naderi2023,
  author =        {Bahman Naderi, Rubén Ruiz, Vahid Roshanaei},
  publisher =     {INFORMS Journal on Computing},
  title =         {Mixed-Integer Programming Versus Constraint Programming for Shop Scheduling Problems: New Results and Outlook},
  year =          {2023},
  doi =           {10.5281/zenodo.7541223},
  url =           {https://github.com/INFORMSJoC/2021-0326},
}  
```

## Description

The goal of this software is to be able to replicate the results of the paper

## Building

It is Python code, so no need to build. However, there is a process to get results. See the Replicating section.

## Results

The results directory contains some python files that are used to parse the txt files obtained as a result. The 7zip "results.7z" contains all the detailed resuls of the paper in detailed logs and text files with all the information.

## Replicating

The source files contain some Python scripts. The entry point is main.py.

main.py takes 9 input arguments. Detailed as follows:

1:	Problem name which can be 'Flowshop','Non-Flowshop','Hybridflowshop','Distributedflowshop','Nowaitflowshop','Setupflowshop','Tardinessflowshop','TCTflowshop','Jobshop','Flexiblejobshop','Openshop','Parallelmachine'

2: 	Model type: 'CP','MIP'

3:  CPU stopping time: an integer with the number of seconds you want the solver to run

4: 	First instance number: integer with the starting instance file name you want to solve

5:  Last instance number: integer with the last instance file name you want to solve

6: 	Solver type: 'CPLEX','Groubi','Google','Xpress'

7:  Number of threads: integer with the number of CPU threads to use in the selected solver

8:  Instance path: Path to the instances files

9:  Results path: Path to the results directory

Example:

python main.py Flexiblejobshop MIP 3600 1 20 CPLEX 4 .\\Instances .\\Results

will solve the MIP model type of the Flexiblejobshop with CPLEX solver with 4 threads, 3600 seconds maximum CPU time for instances from 1.txt to 20.txt in Instances folder and will place the results in Results folder

To automate this process, there are some .bat files that can be invoked. For example "LauncherPython.bat".

We ran all experiments randomly to ensure statistical properties of the results. We generated "configuration files" that are in the scripts folder.
These files contain random sets of argument strings to be fed to main.py through the provided bat files.
