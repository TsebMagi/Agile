# Summer '17 FTP Client


  An insecure FTP client that currently can connect to an ftp server to upload and download a file.
  
  This project uses Python 3.x and uses the Python Crypto library
  
  **SERVER**   
The only way I have currently made the client upload and download files is by running a twisted server on the PSU server.  Anyone can start one of these by getting onto the linux server and using the command:

twistd -n ftp -p 8000 --auth file:pass.dat

The -n keeps the server from being a daemon.  If the CAT is ok with us doing that though, we may be able to just make it a daemon and keep it up permanently.

The port can be any high number between 1024 and 65535 that isn't already used.

The password file is a simple text file you have to create on the linux server that has username:password pairs on each line.  The username must be a valid user name for the server, since twisted will automatically place you in /home/[username] directory when logging in.  The password however, can be anything you want.

By default none of the folders on your home directory on the linux server give you write permissions, so just create a new folder in your /home/[username]/common directory with all permissions (chmod 777 <foldername>).

Options:
connect <host [port] username password>
- used to connect to a server

put <filename filename ...>
- uploads a list of files to the ftp server

get <filename filename ...>
- downloads a list of files from the ftp server

cd <path>
- changes the remote directory

rename <local/remote fromFilename toFilename>
- local fromFilename toFilename will change a local file name
- remote fromFilename toFilename will change a remote file name

create <directoryName>
// TODO

delete <file/folder targetName>
- deletes file or folder specified by targetName

list remote
- list remote directory

list local
- list local directory

save connection
- saves connection info for current server

show connections
- show saved connection information

close
- close connection

quit
- quit program

help
- displays helpful instructions

change <chmod xxx file_name>
- change permissions on file_name to xxx
