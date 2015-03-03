# Introduction #

MSify is an open source client (or dialer) for [Sify Broadband](http://broadband.sify.com/) for GNU/Linux operating system.  This page guides you to install and use MSify.

# Requirements #

You need [Python](http://python.org/) 2.4 or 2.5 to run MSify.  For the graphical interface, PyQt version 4 is required.  On Ubuntu Gutsy, you can install it using ` sudo apt-get install python-qt4 `.  In the current version, MSify can only be launched from command line although the main user interface is graphical.

# Installation #

[Download the latest version](http://msify.googlecode.com/files/msify-1.0.10.zip) of MSify from http://code.google.com/p/msify/downloads/list and extract the archive into a directory in your computer.  Assuming you want to extract the files to ` ~/msify ` directory, this command will extract the files.   (` $ ` is the command prompt.)

```
 $ mkdir ~/msify
 $ unzip -d ~/msify msify-1.0.10.zip
```

Then, edit the ` .sify ` file with an editor like ` kate ` or ` gedit `.  This file has configuration information used by MSify.  You will have to change the values in this file to reflect your settings.
  * ` localip ` specifies the IP address that is allocated to your computer by Sify.
  * ` macaddress ` is the MAC address (or hardware address) of your network card.  You can get this using ` ifconfig ` command (look for HWaddr).  Type this address without any special characters.  For example, if your computer's MAC address is ` 00:11:22:33:44:55 `, type ` 00 11 22 33 44 55 `.
  * ` username ` is your Sify Broadband user name.
  * ` password ` is your password.

```
[network]
localip = 10.14.35.70
macaddress = 00 11 22 33 44 55

[authentication]
username = user_name
password = secret
```

Once these changes are done, installation is complete.

# Usage #

You invoke ` msify.py ` command to login or logout from Sify Broadband.  This section assumes that you have extracted the contents of MSify downloaded archive into ` ~/msify ` directory.

Open the dialer using the following command. (` $ ` is the command prompt.)
```
 $ cd ~/msify
 $ ./msify.py
```

This will open the graphical interface of MSify.  As expected, clicking on _Login_ button logs you in and clicking on _Logout_ logs out of Sify Broadband.

# Frequently Asked Questions #

  * **I get an error saying "_Invalid session,Please relaunch your dialer_" when I try to login.**  Your session has become stale.  Click on _Logout_ button once.  That will fix the problem (which in turn deletes the stale ` .session ` file).
  * **I use a laptop.  How can I change my network settings easily?**  You may find [these directions](http://mankikannan.blogspot.com/2007/08/sify-broadband-client-for-linux.html) useful.
  * **How do I report bugs?** Select ` New Issue ` link on the [Issues](http://code.google.com/p/msify/issues/list) page.

# Fine Print #

MSify is not in any way affiliated with Sify.  Also, MSify is distributed as is without any warranty.  The author of MSify is not liable for any direct or indirect damage caused.