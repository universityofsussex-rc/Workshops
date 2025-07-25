---
title: Basic Exercises 2
permalink: /Exercises/Basic/Exercise2
nav_order: 5
parent: "Basic Exercises"
grand_parent: "Exercises"
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

  <h3 align="center">Basic Exercises #2</h3>
  <p align="center">
    This second set of exercise are designed to get you familiar with the software modules and interactive sessions.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#screen">Screen</a></li>
    <li><a href="#interactive-sessions">Interactive Sessions</a></li>
    <li><a href="#modules-and-software">Modules and Software</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>


## Screen

The first thing when working remotely on a HPC is to handle the inevitable loss of internet that curses all our lives. The screen command creates a detached session running on the remote server so when you disconnect, your session keeps running, and allows you to reconnect to it.


### Starting a screen session 

  Examing the ``screen`` command using ``man`` - start a screen session on the login node called ``workshop`` (flag is called sessionname).

  <details>
  <summary>Hint</summary>

  `screen -S workshop`
  
  </details>

### Detatch screen session 

  Now you have a running session, you could in theory close your terminal/MobaXterm and reconnect. We are going to manually detatch from the screen using ``ctrl+a`` and then press ``d``. If created correctly the output should look like ``[detached from XXXX.workshop]``. 

#### Re-attach to screen session

  So now we have effectively manually interrupted our connection to the screen and want to reconnect to the session. Using ``man`` command, look for the flag that will allow you to resume your screen session.

  <details>
  <summary>Hint</summary>

  <pre><code class="language-bash"> screen -r &lt;sessionname&gt;</code></pre>

  </details>

### Exiting a Screen 

  Our biggest pet peeve on the cluster is old screens hanging around taking up resources.

  Once you have finished working in your screen, simply use the command ``exit`` to close it. 

  Try this now and create a new screen afterwards. 

  Using the command ``man`` and look for the ``list`` flag - with this you can view all screens currently running. Detatch from your screen and run the command to list out all active screens. 

  <details>
  <summary>Hint</summary>

  screen -list

  </details>

  <strong>It should be standard practice to run this command before starting a new screen.</strong>


<p align="right">(<a href="#top">back to top</a>)</p>

## Interactive Sessions


An interactive session is what it sounds like. This allows you to request resources from the HPC schedular to do normal work like a big laptop.

There are many many arguments  - and you should refer to our documentation site <a href="https://artemis-docs.hpc.sussex.ac.uk/artemis/jobs_submission.html">https://artemis-docs.hpc.sussex.ac.uk/artemis/jobs_submission.html</a> for more details.



### Minimum Session 

Within your screen use the ``srun -p workshops --pty bash`` command to start an interactive session. This will start a non-gui capable session with 4GB RAM and 1 Core.

Use the command ``exit`` to end your interactive session.

In future uses, the cluster may be busy - so you might need to wait up to 2h for resources to become free. 

### Asking for more RAM/CPUs 

Sometimes you'll need to do a bit more heavy workloads than editing files and commandline operations. Here we will ask for more cores. 

The schedular can calculate total memory buy multiply cores and RAM requests together. So if you want 30GB and 5 cores, you ask for 6GB per core.

Using the flags shown in the presentation (``--mem-per-cpu``,``-cpus-per-task``), request an interactive session with 6G per core and 4 cores.

Now do the same but ask for 30 cores and 8G per core - what do you see?

The cluster is a shared resource - and as such you are competing for space with others. The more resources you ask for the longer it takes to be allocated, and the lower your priority will become as you use more and more resources within a timescale.

### GUIs 

Sometimes you'll need to be able to view images/graphical user interfaces. This is not possible on Artemis from ssh sessions.

> We do not support commandline X11 GUIs. Please see the Artemis Exercises for the remote desktop for GUIS.



<p align="right">(<a href="#top">back to top</a>)</p>

## Modules and Software

The ``module`` command is the way to load prebuilt software on the HPC provided by your system administrators. Generally you can request for specific software to be installed by a service request to the ITS Service Desk. 

<strong> Clear any sessions and start a new one. Start an interactive session with 2GB and 1 core </strong>


### When Manual Fails 

Sometimes software does not come with a ``man`` entry. Try it now for the ``module`` command.

In this case you'll normally be able to get a similar result by parsing some ``help`` flag. Google is your friend as well - often you'll have no help and will need to google what the args are.

In this case, ``module`` has a help flag ``--help``. Run this now ``module --help``.

### Module Exploring 

There are over 2k software packages installed on Artemis. Because of this you'll need to parse the name, or partial name of software you are looking for, and often will see multiple versions.

In the case of python, not only do you have many versions of the base software, but you'll also have sub modules, and software built with it that will also be returned. 

Run the command:

``module overview python``

To view how many packages for Python there are. 

Now try ``module avail Python`` and ``module avail Python-3``.


The overview command is not case dependent but will only list the number of packages. Avail will list all matching packages and their versions. 


### Module spider 

If you are unsure what a software is - you can explore available packages in even greater detail with the ``module spider`` command. This will give the description of the software, dependencies and often a url to view the homepage.

Run the command:

``module spider python/3``

Here we have to be specific that we only want base python modules and not packages with dependencies on python. 

Take some time to look up software you have used before - it is highly advised you do this now because searching with the module command can be tricky with so many packages.

### Module Display 

Module display is the command to view exactly what a module is going to do to your environment, including variables it is going to assign, any path changes and other modules it depends/conflicts with. 

This is a important command to make sure you dont end up with conflicting packages. We do our best to prevent you from loading packages which conflict, but theres always a way.

Use the module display command to find which packages would be loaded by an ``FSL`` module. (Find a specific version with ``avail`` or ``spider``, then use ``display``).

How would this conflict with ``TensorFlow/1.8.0-foss-2018a-Python-3.6.4``?

Try loading both now with the ``module load`` command.

If you see this message within your normal HPC work - you will have problems eventually. You'll have to use the above commands to find a version that works with your already loaded packages or request for a specific version to be installed for you. This can be avoided with environment managers like ``Anaconda3`` for Python for example.

### Cleaning up your loaded modules 

Sometimes you'll have loaded the wrong modules. You can view what modules you have loaded with ``module list``. Try this now.

You'll see up to 60 loaded modules, with different versions of ``GCCcore`` - which conflict. You'll need to purge your environment with ``module purge``. Run this now and rerun the list command.



### Saving a module list 

You'll generally have a list of go to modules that you'll pretty much always want loaded. You can either create a bash file which has all your ``module load`` commands in. Or you can create a save of it with ``module save <name>`` and ``module restore <name>``.

Load some packages you think you'll be likely to use and try the save, purge, list and restore commands to see how they work.

### More and More 

Investigate the following options with the ``module`` command, what do they do, why would you use them?

```bash
module reset
module is-avail
module savelist
module whatis
ml load Python
```

### Default Modules 

If you do not specify a version when you ``add`` or ``load`` a package, you will be given the default version of that package, which is usually the latest possible version. 

This means you should NEVER use the load command in a shell script without specifying the version, as this could lead to conflicts in 3-6 months when the latest package is installed...



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
