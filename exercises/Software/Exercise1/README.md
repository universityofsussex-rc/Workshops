---
title: Advanced Exercises 1
permalink: /Exercises/Advanced/Exercise1
nav_order: 12
---
<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.

[![Contributors](https://img.shields.io/github/contributors/universityofsussex-its/RC-Workshops.svg?style=for-the-badge)](https://github.com/universityofsussex-its/RC-Workshops/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/universityofsussex-its/RC-Workshops.svg?style=for-the-badge)](https://github.com/universityofsussex-its/RC-Workshops/network/members)
[![Stargazers][stars-shield]][stars-url]
[![Issues](https://img.shields.io/github/issues/universityofsussex-its/RC-Workshops.svg?style=for-the-badge)](https://github.com/universityofsussex-its/RC-Workshops/issues)



<!-- PROJECT LOGO -->

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Software Exercises #1</h3>
  <p align="center">
    This set of exercise will get you ready to install software into your own storage on the cluster. 


  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

| 🚨 🚨 🚨 **NOTE** 🚨 🚨 🚨 |
| :-----------------------------------------: |
| This comes under the advanced tier due to wanting to limit users duplicating software installs in many places. <br> This is useful for when you need software immediately, and cannot wait for the admins to install for you. <br><strong> However always request software via the IT Service Desk Help portal. </strong> |


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#InstallingSoftware">Installing Software</a></li>
    <li><a href="#EasyBuild">EasyBuild</a></li>
  </ol>
</details>




<p align="right">(<a href="#top">back to top</a>)</p>

## Installing Software

All users are more than welcome to install their own software on Lustre (avoid the home directories due to space.) Please do remember that Lustre is not backed up.

Things to remember when installing software:

 - We have many toolchains installed. We reserve the right to update the base system compilers WITHOUT warning. <br> As such, we highly recommend installing against a specific GCC toolchain as a base.
 - Conflicting paths will cause library searches to go awry. When loading software, it should be module environment first, custom second and prefixed. System paths changed by slurm and easybuild will prepend.
 - NFS locking. Make sure that when installling software which creates cache or configs in your NFS home directory - that you are aware we block NFS file locks - as they are non-performative.
 - MPI: Pick MPI < 5... Slurm does not yet have integration with OpenMPI > v4.


### Example Install Exercise

Here will will load modules for the compilers, download the source files and install to a custom directory.

1. First we need to load a compiler. Here I've chosen GCC v 13.3.0 and all the bells and whistles that comes with CMake - we arent going to use CMake, this is just habbit for it to work with other modules which might need more advanced installs.

```bash
srun --pty --cpus-per-task 10 bash
module load CMake/3.29.3-GCCcore-13.3.0
export CC=$(which gcc);export CXX=$(which g++)
echo $CC; echo $CXX
```


2. Now we need to fetch the files and unpack them.

```bash
mkdir /lustre/dir/gsl
wget https://ftp.gnu.org/gnu/gsl/gsl-2.7.1.tar.gz
tar -xvf gsl-2.7.1.tar.gz
cd gsl
```

3. Now we perform a simple configure make. Normally on a personal laptop you wouldnt need the prefix path - however you do not have root access and need to install to a directory owned by you.

```bash

mkdir /lustre/dir/gsl/install
./configure --prefix /lustre/dir/gsl/install
make -j10
make install
```


4. Lastly we make a setup_gsl.sh script. This sets the environment as we installed it, and adds the additional paths to the environment variables.

```bash
#setup_gsl.sh
module load CMake/3.29.3-GCCcore-13.3.0
export CC=$(which gcc);export CXX=$(which g++)
export PATH=/lustre/dir/gsl/install:$PATH
```

You might wonder why we also set the CC and CXX paths - this is so that even if there is a binary that ends up looking for compiler libs - it will point back to the gcc and g++ versions we used to build the software.

<p align="right">(<a href="#top">back to top</a>)</p>

## EasyBuild

We use EasyBuild on the Artemis HPC. You are also welcome to use it to install adittional packages which are simple, and needed quickly. Remember to submit a service request though for it to be built by System Admin specifically for Artemis architecture.

### What is EasyBuild?

EasyBuild is a tool that helps you automatically download, build, and install scientific software (like compilers, libraries, or analysis tools) on Linux systems — especially useful on HPC clusters.

Instead of manually running complicated commands to compile software from source, EasyBuild uses recipes (called EasyConfig files) that describe exactly how to build and install each package and its dependencies.

### Why use EasyBuild?

- Saves time and effort: Automates complex build processes.

- Handles dependencies: Automatically installs software libraries your program needs.

- Keeps software organized: Installs everything cleanly in one place.

- Supports module files: Lets you easily load and switch software versions with environment modules.

- No root required: You can install software in your home directory without admin rights.

### How Does it Work?

You run commands like:

```bash
eb -S GSL
eb Dr GSL-2.7.1.eb 
eb -r GSL-2.7.1.eb
```

This will:

 - Looks for software called GSL in the list of available modules pre-written.
 - Performs a dry run to check what dependencies might need to be installed as well.
 - Performs the install:
    - Downloads the source code for GSL (a math library),
    - Configures and compiles it,
    - Installs it into your BUILD_PATH directory
    - Tests it
    - Moves/Installs it to your INSTALL PATH
    - Creates module files to load the software easily.

### EasyBuild Config

We will want to load the ``EasyBuild`` module. 

When you do so, it wont quite be ready for use. 

Also note - we do not specify a version. Always load the latest EB module.

```bash
module load EasyBuild
eb --show-config
buildpath      (D) = /its/home/<user>/.local/easybuild/build
containerpath  (D) = /its/home/<user>/.local/easybuild/containers
installpath    (D) = /its/home/<user>/.local/easybuild
repositorypath (D) = /its/home/<user>/.local/easybuild/ebfiles_repo
robot-paths    (D) = /mnt/shared/easybuild/software/EasyBuild/5.0.0/easybuild/easyconfigs
rpath          (D) = True
sourcepath     (D) = /its/home/<user>/.local/easybuild/sources
```

As you can see here, easybuild has attempted to configure itself in a user environment, however we need to make a config file for it to work for a user, and pull from our existing global config.

Create a file ``~/.config/easybuild/config.cfg``:

```bash
[config]
installpath = /mnt/lustre/users/<dep>/<user>/easybuild/
buildpath = /mnt/lustre/users/<dep>/<user>/easybuild/build
sourcepath = /mnt/lustre/users/<dep>/<user>/easybuild/sources
containerpath = /mnt/lustre/users/<dep>/<user>/easybuild/containers
```

Now create those directories.

To use modules you install this way, simply extend the ``MODULEPATH`` variable with your install path. eg ``export MODULEPATH=$MODULEPATH:/mnt/lustre/users/<dep>/<user>/easybuild/modules``

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/universityofsussex-its/RC-Workshops.svg?style=for-the-badge
[contributors-url]: https://github.com/universityofsussex-rc/Workshops/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/universityofsussex-its/RC-Workshops.svg?style=for-the-badge
[forks-url]: https://github.com/universityofsussex-rc/Workshops/network/members
[stars-shield]: https://img.shields.io/github/stars/universityofsussex-its/RC-Workshops.svg?style=for-the-badge
[stars-url]: https://github.com/universityofsussex-rc/Workshops/stargazers
[issues-shield]: https://img.shields.io/github/issues/universityofsussex-its/RC-Workshops.svg?style=for-the-badge
[issues-url]: https://github.com/universityofsussex-rc/Workshops/issues