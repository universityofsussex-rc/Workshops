---
title: Artemis Exercises 1
permalink: /Artemis/Exercise1
nav_order: 8
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

  <h3 align="center">Artemis Exercises #1</h3>
  <p align="center">
    This first set of exercise will get you logged into the Open OnDemand Web Portal and Navigate you through each Service.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#login">Login</a></li>
    <li><a href="#landing-page">Landing Page</a></li>
    <li><a href="#files">Files</a></li>
    <li><a href="#jobs">Jobs</a></li>
    <li><a href="#clusters">Clusters</a></li>
    <li><a href="#interactive-apps">Interactive Apps</a></li>
    <li><a href="#monitoring">Monitoring</a></li>
    <li><a href="#summary">Summary</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

## Login

<p>
  Access to the Artemis Hybrid Research Cluster (HRC) is expected to be primarily be via your browser, and if off campus, using the VPN. If you currently do not have access to the VPN - you will need to request as such, and to be added to the relevant departmental group in Palo Alto. It is assumed you either have access now, or are on campus.    
</p>

### Open OnDemand

<p>

You will need to access the Open OnDemand Web Portal - via <a href="https://ood.artemis.hrc.sussex.ac.uk">ood.artemis.hrc.sussex.ac.uk</a>. You will need to login with your usual Sussex Username and password. Unfortunately if you are unable to login - this means you currently do not have an account and will need to request one. Please see <a href="https://artemis-docs.hpc.sussex.ac.uk/artemis/access.html">Getting Access</a> page in our documentation.

</p>

### SSH

<p>

Similarly to the old Apollo2 HPC, Artemis has login nodes for direct command line access to the cluster. You can reach this using the same address as above. You will still either need to be on campus, or logged into the Staff VPN.
</p>

```
bash-4.2$ ssh anon123@ood.artemis.hrc.sussex.ac.uk
```

## Landing Page
<p>
The landing page should look like:
</p>
<p align="center">
<img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/ood-splash.PNG"/>
</p>
<p>

This page will display various message of the day, will have common apps and services pinned to the bar, and have navigation links to our documentation site <a href="https://artemis-docs.hrc.sussex.ac.uk/artemis">https://artemis-docs.hrc.sussex.ac.uk/artemis</a>.

In the navigation bar at the top you have the following options:
</p>

<ul>
<li>
  <h4>artemis:</h4>
  <p>
  Clicking this will navigate to the Open OnDemand (OOD) landing page.
  </p>
</li>
<li>
  <h4>Files:</h4>
  <p>
  Opens a dropdown menu with links to access the files and folders in your attached storage/home/lustre directories on the HRC.
  </p>
</li>
<li>
  <h4>Jobs:</h4>
  <p>
  Opens the Jobs dropdown which has navigable links to the Active Jobs monitoring page, and the Jobs Composer - which allows you to craft batch jobs in the browser from templates and previous jobs.
  </p>
</li>
<li>
  <h4>Clusters:</h4>
  <p>
  Opens cluster selection dropdown. Access to the Login nodes commandline of the production or other project based clusters. (Currently only the production cluster - artemis)
  </p>
</li>
<li>
  <h4>Interacitve Apps:</h4>
  <p>
  Opens the app selector. Currently has three options - Jupyter Notebooks and Remote Desktop (XFCE) and the DEV version of the Remote Desktop.
  </p>
</li>
<li>
  <h4>Monitoring:</h4>
  <p>
  This will provide links to dashboard powered by Prometheus and Grafana. This can be used to monitor cluster usage, load, jobs, job resource consumption, downtime etc. 
  </p>
</li>
<li>
  <h4>Two Blocks Icon:</h4>
  <p>
  Clicking this will navigate to the "My Interactive Session" - this page lists any sessions launched from the Interactive Apps drop-down.
  </p>
</li>
<li>
  <h4>Options:</h4>
  <p>
   Opens a dropdown menu which will provide links to the ticketing service, online documentation. This option also includes a Restart Web Server option which will refresh you session.
  </p>
</li>
<li>
  <h4>Logout Logo:</h4>
  <p>
  Quite simple really - the logout and close session. You might need to clear cookies for the account to completely logout.
  </p>
</li>

</ul>

<p align="right">(<a href="#top">back to top</a>)</p>


## Files

<p align="center">
<img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/files-menu.PNG" />
</p>

The Files menu allows exploration, edit, upload of files and folders into the HRC environment. 

Currently you will have you home directory, and links to your lustre and lustre scratch spaces. 

You can access any of the remote mounted storage from this page, by clicking "Change Directory".


### Files Excercises

   1. Workshop Working Directory:

      Please make a directory in your home folder called "HPC-Workshop". This is so that an admin can find and locate the files during the workshop. 
    
      1. Make a directory inside `/home/<user>/HPC-Workshop/` which will be your work directory for the duration of the Workshop only. At the end of the Workshop you can download the folder if needed. We will refer to this directory as the `workdir`.

      1. Navigate into your `workdir` and upload a **small** file from your desktop. 

      1. Navigate back up to the `HPC-Workshop` folder and click the checkbox next to your `workdir`. Now download. You should download a zip containing your uploaded file.

      1. Copy your current path using the `copy path` button. Now Change directory to the shared software directory `/mnt/shared`. 

      1. Navigate back, and create a file `README.txt` in your workdir. Click the three dots next to your new file and edit. Write a brief explanation of what the contents of this folder will contain for future reference. Don't forget to click save in the top-left.

      1.If you need to, navigate back to your `workdir` by pasting the copied path from earlier. Make two directories in your workdir `Jobs` and `Templates`. You might need these later to save your work after the workshop.


<p align="right">(<a href="#top">back to top</a>)</p>

## Jobs

2.  Navigating the Jobs Pages.

    1. Navigate to the Active Jobs page via the Jobs dropdown menu in the navigation bar. 

        You should see somthing like:

        <p align="center">
        <img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/active-jobs.PNG"/>
        </p>

        This page lists any active job in the queue, with selection for each cluster, and allows the user some basic filter options. Depending on the current progress of other users in the Workshop - you may or may not see some jobs active.

    2. Navigate to the Jobs Composer via the same dropdown menu in the navigation bar.

        This will either redirect or open a new tab and you should see a page similar to:

        <p align="center">
        <img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/jobs-composer.PNG"/>
        </p>

    3. Navigate in the new grey navigation menu to `Templates` - again you should see something similar to:

        <p align="center">
        <img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/jobs-templates.png"/>
        </p>

    4. Either close the tab, or click the `Open OnDemand` in the top right to navigate back to the Dashboard.

<p align="right">(<a href="#top">back to top</a>)</p>


## Clusters

3. Artemis Browser Shell

    1. Using the `Clusters` dropdown - start an interactive shell session on one of the production cluster login nodes.

        <p align="center">
        <img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/prd_shell.png" align/>
        </p>

        You should now have a command line shell on one of the `artemis-login-0` nodes.

        <p align="center">
        <img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/shell.PNG" class="centre" />
        </p>

    2. Navigate to your `workdir`, using simple bash commands. Listing the directory should show 2 folders and 2 files. 

    3. Test out the `module` command and load a package. 

|  ⚠️ Warning ⚠️  |
| :-----------: |
| **IMPORTANT:** Some browsers like Google Chrome will force a tab into the background while you are not actively using it - these causes the shell session to  terminate early. You can change this is setting, or start a `screen` or `tmux` session and just refresh the shell page to resume. |

<p align="right">(<a href="#top">back to top</a>)</p>


## Shell

4. Artemis SSH Session

    1. If you can, start a terminal on your computer (Xterm, Terminal, MobaXterm.. etc.). Using the `ssh` command, log into the Artemis login node.
    2. Do you have any module not found or module not available errors? Why might this be? Check the documentation FAQs for what can cause this!
    3. Using your shell, load a piece of software of your choosing. Use the `module list` command to view what packages have automatically been loaded for you.
    4. Depending on the package you loaded, you might see 30 or more additional modules loaded for that software to work. Now see if you can find a software module which will load more than 200+ from a single load command. (Make sure to purge after each load to not conflict modules).


## Interactive Apps

This dropdown provides access to one of the key tools that Open OnDemand will provide that was lacking in the Apollo2 HPC. Currently available are a Remote-Desktop tool provided by XFCE and a Jupyter Notebook server.

<p align="center">
<img src="https://universityofsussex-rc.github.io/Workshops/images/sge-slurm/dd-interactive-apps.PNG"/>
</p>

## Monitoring

Provides Dashboards for project owners. Have an explore - but we won't be deep diving during this workshop.

## Summary

Hopefully now you have a brief overview of what the Open OnDemand Web Portal can provide in terms of access to the cluster. 

The rest of the exercises in this workshop will focus on the user of the Jobs and Interactive sessions services provided by OOD. 


 You should now have an understanding of:

 - File access:
    - Navigation
    - Creation
    - Edit
    - Uploads
    - Downloads
 - Navigation Dropdowns
    - Files
    - Jobs
    - Cluster
    - Interactive Apps
 - Accesing the Artemis Login Nodes via in Browser Shell
 - Accesing the Artemis Login Nodes via in local terminal Shell




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
