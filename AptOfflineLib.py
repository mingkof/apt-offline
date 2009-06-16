import os
import sys

import threading
import Queue

import zipfile
import bz2
import gzip

# Test Comment
# For Forest

WindowColor = True
try:
        import WConio
except ImportError:
        WindowColor = False
    

from array import array
import signal

#INFO: They aren't on Windows
try:
        from fcntl import ioctl
        import termios
except ImportError:
        pass
    

#INFO: Python 2.5 introduces hashlib.
# This module supports many hash/digest algorithms
# We do this check till Python 2.5 becomes widely used.
Python_2_5 = True
try:
        import hashlib
except ImportError:
        Python_2_5 = False
    
    
class Checksum:
        
        def HashMessageDigestAlgorithms( self, checksum, HashType, file ):
                data = open( file, 'rb' )
                if HashType == "sha256":
                        Hash = self.sha256( data )
                elif HashType == "md5":
                        Hash = self.md5( data )
                else: Hash = None
                data.close()
                
                if Hash == checksum:
                        return True
                return False
        
        def sha256( self, data ):
                hash = hashlib.sha256()
                hash.update( data.read() )
                return hash.hexdigest()
        
        def md5( self, data ):
                hash = hashlib.md5.new()
                hash.update( data.read() )
                return hash.hexdigest() 
        
        def CheckHashDigest( self, file, checksum ):
                type = checksum.split(":")[0]
                type = type.lower()
                checksum = checksum.split( ":" )[1]
                return self.HashMessageDigestAlgorithms( checksum, type, file )
        

class Log:
        '''A OOP implementation for logging.
            warnings is to tackle the warning option
            verbose is to tackle the verbose option
            color is if you want to colorize your output
    
            You should pass these options, taking it from optparse/getopt,
            during instantiation'''
            
        #            WConio can provide simple coloring mechanism for Microsoft Windows console
        #            Color Codes:
        #            Black = 0
        #            Green = 2
        #            Red = 4
        #            White = 15
        #            Light Red = 12
        #            Light Cyan = 11
        #            
        #            #FIXME: The Windows Command Interpreter does support colors natively. I think that support has been since Win2k.
        #            That's all for Windows Command Interpreter.
        #            
        #            As for ANSI Compliant Terminals (which most Linux/Unix Terminals are.).....
        #            I think the ANSI Color Codes would be good enough for my requirements to print colored text on an ANSI compliant terminal.
        #
        #            The ANSI Terminal Specification gives programs the ability to change the text color or background color.
        #            An ansi code begins with the ESC character [^ (ascii 27) followed by a number (or 2 or more separated by a semicolon) and a letter.
        #    
        #            In the case of colour codes, the trailing letter is "m"...
        #    
        #            So as an example, we have ESC[31m ... this will change the foreground colour to red.
        #    
        #            The codes are as follows:
        #    
        #            For Foreground Colors
        #            1m - Hicolour (bold) mode
        #            4m - Underline (doesn't seem to work)
        #            5m - BLINK!!
        #            8m - Hidden (same colour as bg)
        #            30m - Black
        #            31m - Red
        #            32m - Green
        #            33m - Yellow
        #            34m - Blue
        #            35m - Magenta
        #            36m - Cyan
        #            37m - White
        #    
        #            For Background Colors
        #    
        #            40m - Change Background to Black
        #            41m - Red
        #            42m - Green
        #            43m - Yellow
        #            44m - Blue
        #            45m - Magenta
        #            46m - Cyan
        #            47m - White
        #    
        #            7m - Change to Black text on a White bg
        #            0m - Turn off all attributes.
        #    
        #            Now for example, say I wanted blinking, yellow text on a magenta background... I'd type ESC[45;33;5m
        
        def __init__( self, verbose, lock=None ):
                self.VERBOSE = bool( verbose )
                self.color_syntax = '\033[1;'
                
                if lock is True:
                        self.DispLock = threading.Lock()
                        self.lock = True
                else:
                        self.DispLock = False
                        self.lock = False
                
                if os.name == 'posix':
                        self.platform = 'posix'
                        self.color = {'Red': '31m', 'Black': '30m',
                                      'Green': '32m', 'Yellow': '33m',
                                      'Blue': '34m', 'Magneta': '35m',
                                      'Cyan': '36m', 'White': '37m',
                                      'Bold_Text': '1m', 'Underline': '4m',
                                      'Blink': '5m', 'SwitchOffAttributes': '0m'}
           
                elif os.name in ['nt', 'dos']:
                        self.platform = None
            
                        if WindowColor is True:
                                self.platform = 'microsoft'
                                self.color = {'Red': 4, 'Black': 0,
                                              'Green': 2, 'White': 15,
                                              'Cyan': 11, 'SwitchOffAttributes': 15}
                else:
                        self.platform = None
                        self.color = None
        
        def set_color( self, color ):
                '''Check the platform and set the color'''
                if self.platform == 'posix':
                        sys.stdout.write( self.color_syntax + self.color[color] )
                        sys.stderr.write( self.color_syntax + self.color[color] )
                elif self.platform == 'microsoft':
                        WConio.textcolor( self.color[color] )
        
        def msg( self, msg ):
                '''Print general messages. If locking is available use them.'''
                if self.lock:
                        self.DispLock.acquire( True )
          
                self.set_color( 'White' )
                sys.stdout.write( msg )
                sys.stdout.flush()
                self.set_color( 'SwitchOffAttributes' )
        
                if self.lock:
                        self.DispLock.release()
        
        def err( self, msg ):
                '''Print messages with an error. If locking is available use them.'''
                if self.lock:
                        self.DispLock.acquire( True )
            
                self.set_color( 'Red' )
                sys.stderr.write( "ERROR: " + msg )
                sys.stderr.flush()
                self.set_color( 'SwitchOffAttributes' )
        
                if self.lock:
                        self.DispLock.release()
        
        def success( self, msg ):
                '''Print messages with a success. If locking is available use them.'''
                if self.lock:
                        self.DispLock.acquire( True )
            
                self.set_color( 'Green' )
                sys.stdout.write( msg )
                sys.stdout.flush()
                self.set_color( 'SwitchOffAttributes' )
        
                if self.lock:
                        self.DispLock.release()
        
        # For the rest, we need to check the options also
        def verbose( self, msg ):
                '''Print verbose messages. If locking is available use them.'''
                if self.lock:
                        self.DispLock.acquire( True )
                
                if self.VERBOSE is True:
                        self.set_color( 'Cyan' )
                        sys.stdout.write( "VERBOSE: " + msg )
                        sys.stdout.flush()
                        self.set_color( 'SwitchOffAttributes' )
        
                if self.lock:
                        self.DispLock.release()
        
        def calcSize( self, size ):
                ''' Takes number of kB and returns a string
                of proper size. Like if > 1024, return a megabyte '''
                if size > 1024:
                        size = size // 1024
                        if size > 1024:
                                size = size // 1024
                                return ( "%d GiB" % ( size ) )
                        return ( "%d MiB" % ( size ) )
                return ( "%d KiB" % ( size ) )


class ProgressBar( object ):
        
        def __init__( self, minValue=0, maxValue=0, width=None, fd=sys.stderr ):
                #width does NOT include the two places for [] markers
                self.min = minValue
                self.max = maxValue
                self.span = float( self.max - self.min )
                self.fd = fd
                self.signal_set = False
        
                if width is None:
                        try:
                                self.handle_resize( None, None )
                                signal.signal( signal.SIGWINCH, self.handle_resize )
                                self.signal_set = True
                        except:
                                self.width = 79 #The standard
                
                else:
                        self.width = width
            
                self.value = self.min
                self.items = 0 #count of items being tracked
                self.complete = 0
        
        def handle_resize( self, signum, frame ):
                h, w = array( 'h', ioctl( self.fd, termios.TIOCGWINSZ, '\0' * 8 ) )[:2]
                self.width = w
    
        def updateValue( self, newValue ):
                #require caller to supply a value! newValue is the increment from last call
                self.value = max( self.min, min( self.max, self.value + newValue ) )
                self.display()
        
        def completed( self ):
                self.complete = self.complete + 1
        
                if self.signal_set:
                        signal.signal( signal.SIGWINCH, signal.SIG_DFL )
                self.display()
        
        def addItem( self, maxValue ):
                self.max = self.max + maxValue
                self.span = float( self.max - self.min )
                self.items = self.items + 1
                self.display()
        
        def display( self ):
                print "\r%3s/%3s items: %s\r" % ( self.complete, self.items, str( self ) ),
        
        def __str__( self ):
                #compute display fraction
                percentFilled = ( ( self.value - self.min ) / self.span )
                widthFilled = int( self.width * percentFilled + 0.5 )
                return ( "[" + "#"*widthFilled + " " * ( self.width - widthFilled ) + "]" + " %5.1f%% of  %s" % ( percentFilled * 100.0, self.__numStr__( self.max / 1024 ) ) )
        
        def __numStr__( self, size ):
                if size > 1024:
                        size = size / 1024
                        if size > 1024:
                                size = size / 1024
                                return ( "%d GiB" % ( size ) )
                        return ( "%d MiB" % ( size ) )
                return ( "%d KiB" % ( size ) )


class Archiver:
        def __init__( self, lock=None ):
                if lock is None or lock != 1:
                        self.ZipLock = False
                else:
                        self.ZipLock = threading.Lock()
                        self.lock = True
        
        def TarGzipBZ2_Uncompress( self, SourceFileHandle, TargetFileHandle ):
                try:
                        TargetFileHandle.write( SourceFileHandle.read() )
                except EOFError:
                        pass
                return True
        
        def compress_the_file( self, zip_file_name, files_to_compress ):
                '''Condenses all the files into one single file for easy transfer'''
        
                try:
                        if self.lock:
                                self.ZipLock.acquire( True )
                        filename = zipfile.ZipFile( zip_file_name, "a" )
                except IOError:
                        #INFO: By design zipfile throws an IOError exception when you open
                        # in "append" mode and the file is not present.
                        filename = zipfile.ZipFile( zip_file_name, "w" )
                finally: #Supported from Python 2.5 ??
                        filename.write( files_to_compress, os.path.basename( files_to_compress ), zipfile.ZIP_DEFLATED )                        
                        filename.close()
        
                        if self.lock:
                                self.ZipLock.release()
            
                        return True

        def decompress_the_file( self, archive_file, path, target_file, archive_type ):
                '''Extracts all the files from a single condensed archive file'''
                if archive_type == "bzip2":
                        try:
                                read_from = bz2.BZ2File( archive_file, 'r' )
                        except IOError:
                                return False
                                    
                        try:
                                write_to = open ( os.path.join( path, target_file ), 'wb' )
                        except IOError:
                                return False
                        
                        if self.TarGzipBZ2_Uncompress( read_from, write_to ) != True:
                                #FIXME:
                                raise ArchiveError
                        write_to.close()
                        read_from.close()
                        return True
                elif archive_type == "gzip":
                        try:
                                read_from = gzip.GzipFile( archive_file, 'r' )
                        except IOError:
                                return False
                        try:
                                write_to = open( os.path.join( path, target_file ), 'wb' )
                        except IOError:
                                return False
                        
                        if self.TarGzipBZ2_Uncompress( read_from, write_to ) != True:
                                #FIXME:
                                raise ArchiveError
                        write_to.close()
                        read_from.close()
                        return True
                elif archive_type == "zip":
                        # FIXME: This looks odd. Where are we writing to a file ???
                        try:
                                zip_file = zipfile.ZipFile( file, 'rb' )
                        except IOError:
                                return False
                        
                        #FIXME:
                        for filename in zip_file.namelist():
                                data = zip_file.read()
                        zip_file.close()
                        return True
                else:
                        return False

class FileMgmt( object ):
        
        def __init__( self ):
                self.duplicate_files = []

        def files( self, root ): 
                for path, folders, files in os.walk( root ): 
                        for file in files: 
                                yield path, file 

        def find_first_match( self, cache_dir=None, filename=None ):
                '''Return the full path of the filename if a match is found
                Else Return False'''
                if cache_dir is None:
                        return False
                elif filename is None:
                        return False
                elif os.path.isdir( cache_dir ) is False:
                        return False
                else:
                        for path, file in self.files( cache_dir ): 
                                if file == filename:
                                        return os.path.join( path, file )
                                return False
        
        def rename_file( self, orig, new ):
                '''Rename file from orig to new'''
                if not os.path.isfile( orig ):
                        return False
                os.rename( orig, new )
                return True

        def remove_file( self, src ):
                '''Remvoe the given src file.'''
                try:
                        os.unlink( src )
                except IOError:
                        return False

        def move_file( self, src, dest ):
                '''Move file from src to dest.'''
                if not os.path.isdir( dest ):
                        return False
                try:
                        os.rename( src, dest + "/" + os.path.basename( src ) )
                except IOError:
                        return False
                
        def move_folder( self, src, dest ):
                '''Move folder from src to dest.'''
                if os.path.isdir( dest ):
                        try:
                                os.rename( src, dest + "/" + os.path.basename( src ) )
                        except IOError:
                                return False

        def find_dup( self, dir ):
                '''"dir" will be the directory withing which duplicate files are searched
                Returns a list with the duplicates'''
        
                #TODO: This is buggy currently
    
                for xpath, yfile in dir:
            
                        for path, file in dir:
                                if file == yfile:
                                        if not ( xpath + "/" + yfile == path + "/" + file ):
                                                if [xpath + "/" + yfile, path + "/" + file] in self.duplicate_files:
                                                        break
                                        else:
                                                self.duplicate_files += [ [xpath + "/" + yfile, path + "/" + file] ]
                                        #self.duplicate_files = set(self.duplicate_files)
                
                len = self.duplicate_files.__len__()
                print len
                for x in range( len ):
                        self.duplicate_files[x].sort()
                self.duplicate_files.sort()
                num = 0
                number = 0
                for ( x, y ) in self.duplicate_files:
                        while number < len - 1:
                                if x in self.duplicate_files[number] or y in self.duplicate_files[number]:
                                        num += 1
                                        print num
                                        if num > 1:
                                                print "Num went 2"
                                                self.duplicate_files.pop( number )
                                                num -= 0
                                number += 1
    
                return self.duplicate_files

class MyThread( threading.Thread ):
        """My thread class"""
        def __init__( self, requestQueue, responseQueue, WorkerFunction, NumOfThreads=1 ):
                # Pool of NUMTHREADS Threads that run run().
                self.requestQueue = requestQueue
                self.responseQueue = responseQueue
                self.threads = NumOfThreads
                self.WorkerFunction = WorkerFunction
                self.thread_pool = [
                       threading.Thread( 
                              target=self.run,
                              args=( self.requestQueue, self.responseQueue )
                              )
                       for i in range( self.threads )
                       ]
        
        def startThreads( self ):
                for thread in self.thread_pool:
                        thread.start()
                
        def stopThreads( self ):
                '''Shut down the threads after all requests end.
                (Put one None "sentinel" for each thread.)'''
                for thread in self.thread_pool:
                        self.requestQueue.put( None )
                        
        def populateQueue( self, item ):
                self.requestQueue.put( item )
                
        def stopQueue( self ):
                '''Don't end the program prematurely.
                (Note that because Queue.get() is blocking by
                defualt this isn't strictly necessary. But if
                you were, say, handling responses in another
                thread, you'd want something like this in your
                main thread.)'''
                for thread in self.thread_pool:
                        thread.join()
                        
        def run( self, requestQueue, responseQueue ):
                while True:
                        item = requestQueue.get()
                        if item is None:
                                break
                        thread_name = threading.currentThread().getName()
                        responseQueue.put( self.WorkerFunction( item, thread_name ) )
                        
                        exit_status = responseQueue.get()