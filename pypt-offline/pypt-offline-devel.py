#!/usr/bin/env python
# pypt-offline.py
# version devel
# Release: svn_tagging_test

############################################################################
#    Copyright (C) Ritesh Raj Sarraf                                       #
#    rrs@researchut.com                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software F[-d] [-s] [-u]oundation, Inc.,                         #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import os, sys, optparse, pypt_core


if __name__ == "__main__":
    
    try:
        version = "0.6b"
        reldate = "03/10/2005"
        copyright = "(C) 2005 Ritesh Raj Sarraf - RESEARCHUT (http://www.researchut.com/)"
    
        #FIXME: Option Parsing
        # There's a flaw with either optparse or I'm not well understood with it
        # Presently you need to provide all the arguments to it to work.
        # No less, no more. This needs to be converted to getopt sometime.
        
        #parser = OptionParser()
        #parser = optparse.OptionParser()
        parser = optparse.OptionParser(usage="%prog [OPTION1, OPTION2, ...]", version="%prog " + version)
        parser.add_option("-d","--download-dir", dest="download_dir", help="Root directory path to save the downloaded files", action="store", type="string", metavar="pypt-downloads")
        #parser.set_defaults(download_dir="pypt-downloads")
        parser.add_option("-s","--cache-dir", dest="cache_dir", help="Root directory path where the pre-downloaded files will be searched. If not, give a period '.'",action="store", type="string", metavar=".")
        #parser.set_defaults(cache_dir=".")
        #parser.set_defaults(cache_dir=".")
        parser.add_option("-u","--uris", dest="uris_file", help="Full path of the uris file which contains the main database of files to be downloaded",action="store", type="string")
        
        #TODO: Add updation
        # The new plan is to make pypt-offline do the updation and upgradation from within its own interface instead of expecting
        # the user to do the dirty part. We'll add options which'll take care of it.
        # For this we'll have additional options
        # --set-update - This will extract the list of uris which need to be fetched for _updation_. This command must be executed on the NONET machine.
        # --fetch-update - This will fetch the list of uris which need for apt's databases _updation_. This command must be executed on the WITHNET machine.
        # --install-update - This will install the fetched database files to the  NONET machine and _update_ the apt database on the NONET machine. This command must be executed on the NONET machine.
        # The same will happen for upgradation.
        # --set-upgrade - This will extract the list of uris which need to be fetched for _upgradation_. This command must be executed on the NONET machine.
        # --fetch-upgrade - This will fetch the list of uris which need for apt's databases _upgradation_. This command must be executed on the WITHNET machine.
        # --install-upgrade - This will install the fetched database files to the  NONET machine and _upgrade_ the packages. This command must be executed on the NONET machine.
        parser.add_option("","--set-update", dest="set_update", help="Extract the list of uris which need to be fetched for _updation_", action="store", type="string", metavar="pypt-offline-update.dat")
        #parser.set_defaults(set_update="pypt-offline-update.dat")
        parser.add_option("","--fetch-update", dest="fetch_update", help="Fetch the list of uris which are needed for apt's databases _updation_. This command must be executed on the WITHNET machine", action="store", type="string", metavar="pypt-offline-update.dat")
        #parser.set_defaults(fetch_update="pypt-offline-update.dat")
        parser.add_option("","--install-update", dest="install_update", help="Install the fetched database files to the  NONET machine and _update_ the apt database on the NONET machine. This command must be executed on the NONET machine", action="store", type="string", metavar="pypt-offline-update-fetched.zip")
        #parser.set_defaults(install_update="pypt-offline-update-fetched.zip")
        parser.add_option("","--set-upgrade", dest="set_upgrade", help="Extract the list of uris which need to be fetched for _upgradation_", action="store", type="string", metavar="pypt-offline-upgrade.dat")
        #parser.set_defaults(set_upgrade="pypt-offline-upgrade.dat")
        parser.add_option("","--upgrade-type", dest="upgrade_type", help="Type of upgrade to do. Use one of upgrade, dist-upgrade, dselect-ugprade", action="store", type="string", metavar="upgrade")
        #parser.set_defaults(upgrade_type="upgrade")
        parser.add_option("","--fetch-upgrade", dest="fetch_upgrade", help="Fetch the list of uris which are needed for apt's databases _upgradation_. This command must be executed on the WITHNET machine", action="store", type="string", metavar="pypt-offline-upgrade.dat")
        #parser.set_defaults(fetch_upgrade="pypt-offline-upgrade.dat")
        parser.add_option("","--install-upgrade", dest="install_upgrade", help="Install the fetched packages to the  NONET machine and _upgrade_ the packages on the NONET machine. This command must be executed on the NONET machine", action="store", type="string", metavar="pypt-offline-update-fetched.zip")
        #parser.set_defaults(install_ugprade="pypt-offline-update-fetched.zip")
        (options, args) = parser.parse_args()
        #parser.check_required("-d", "-s", "-u")
        #if len(arguments) != 2:
        #    parser.error("Err! Incorrect number of arguments. Exiting")
        #print len(args)
        #if len(options) != 1 or len(options) > 2:
        #    print len(args)
        #    parser.error("No arguments were passed\n")
        #    sys.exit(1)
            
        
        #sRawUris = options.uris_file
        #if sRawUris is None:
        #    if os.access("pypt-offline-update.dat", os.R_OK) is True:
        #        sRawUris = "pypt-offline-update.dat"
        
            
        sys.stdout.write("pypt-offline %s\n" % (version))
        sys.stdout.write("Copyright %s\n" % (copyright))
        
        if options.set_update:
            if os.getuid() != 0:
                parser.error("This option requires super-user privileges. Execute as root or use sudo/su")
                
            if sys.platform == "linux2" or sys.platform == "gnu0" or sys.platform == "gnukfreebsd5":
                sys.stdout.write("Generating database of files that are needed for an update.\n")
                os.chdir(options.set_update)
                os.system('/usr/bin/apt-get -qq --print-uris update > pypt-offline-update.dat')
            else:
                parser.error("This argument is supported only on Unix like systems with apt installed\n")
                #TODO: Implement --set-update using _maybe_ apt
            sys.exit(0)

        if options.set_upgrade or options.upgrade_type:
            if not (options.set_upgrade and options.upgrade_type):
                parser.error("Options --set-upgrade and --upgrade-type are mutually inclusive\n")
            else:
                if os.getuid() != 0:
                    parser.error("This option requires super-user privileges. Execute as root or use sudo/su")
                
                if sys.platform == "linux2" or sys.platform == "gnu0" or sys.platform == "gnukfreebsd5":
                    os.chdir(options.set_upgrade)
                    if options.upgrade_type == "upgrade":
                        sys.stdout.write("Generating database of files that are needed for an upgrade.\n")
                        os.system('/usr/bin/apt-get -qq --print-uris upgrade > pypt-offline-upgrade.data')
                    elif options.upgrade_type == "dist-upgrade":
                        sys.stdout.write("Generating database of files that are needed for an upgrade.\n")
                        os.system('/usr/bin/apt-get -qq --print-uris dist-upgrade > pypt-offline-upgrade.data')
                    elif options.upgrade_type == "dselect-upgrade":
                        sys.stdout.write("Generating database of files that are needed for an upgrade.\n")
                        os.system('/usr/bin/apt-get -qq --print-uris dselect-upgrade > pypt-offline-upgrade.data')
                    else:
                        parser.error("Invalid upgrade argument type selected\nPlease use one of, upgrade/dist-upgrade/dselect-upgrade\n")
                else:
                    parser.error("This argument is supported only on Unix like systems with apt installed\n")
                sys.exit(0)
            
        if options.fetch_update:
            #TODO: Updation
            # Implement below similar code for updation
            sys.stdout.write("\nFetching uris which update apt's package database\n\n")
            
            # Since we're in fetch_update, the download_type will be non-deb/rpm data
            # 1 is for update packages 
            # 2 is for upgrade packages
            download_type = 1
            pypt_core.starter(options.fetch_update, options.download_dir, options.cache_dir, download_type)
            
        if options.fetch_upgrade:
            sys.stdout.write("\nFetching packages which need upgradation\n\n")
            
            # Since we're in fetch_update, the download_type will be non-deb/rpm data
            # 1 is for update packages 
            # 2 is for upgrade packages
            download_type = 2
            pypt_core.starter(options.fetch_upgrade, options.download_dir, options.cache_dir, download_type)
    
    except KeyboardInterrupt:
        sys.stderr.write("\nReceived immediate EXIT signal. Exiting!\n")
        sys.exit(1)