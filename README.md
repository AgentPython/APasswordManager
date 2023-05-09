# Kault

Kault is a simple Python password manager. It allows you to securely save secrets with a simple CLI interface.

## Features

 - Secrets are stored in an encrypted SQLite database with [SQLCipher](https://www.zetetic.net/sqlcipher/)
 - Within the database, each password and notes are encrypted with a unique salt using AES-256 encryption with [pycryptodome](http://legrandin.github.io/pycryptodome/)
 - Master key is hashed with a unique salt
 - Possibility to create an unlimited number of vaults
 - Clipboard cleared automatically
 - Automatic vault locking after inactivity
 - Password suggestions with [password-generator-py](https://github.com/gabfl/password-generator-py)
 - Import / Export in Json, Yaml, Kault (DB)

 ## Basic usage

 ##### Coming soon

 ## Installation and setup

 Kault 0.1.* requires `sqlcipher` to be installed on your machine.

 Requirement:
 - OpenSSL
 - Tcl

 ### MacOS

On MacOS, you can install `sqlcipher` with [brew](https://brew.sh/):
```bash
brew install sqlcipher

# If you are getting an error "Failed to build sqlcipher3", you would need to fix the build flags:
SQLCIPHER_PATH="$(brew --cellar sqlcipher)/$(brew list --versions sqlcipher | tr ' ' '\n' | tail -1)"
C_INCLUDE_PATH=$SQLCIPHER_PATH/include LIBRARY_PATH=$SQLCIPHER_PATH/lib
```

### Ubuntu / Debian

On Ubuntu/Debian, you can install `sqlcipher` with apt:
```bash
sudo apt update
sudo apt install -y gcc python3-dev libsqlcipher-dev xclip
```

or you can install manually from `sqlcipher` repository:

```bash
$ git clone https://github.com/sqlcipher/sqlcipher.git
$ ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC" \
	LDFLAGS="-lcrypto"
$ make
$ sudo make install
```

### Windows

On Windows, you can only install `sqlcipher` manually. \
<small>*Note: only available for 64 bit*</small>

#### Building
1. Open Visual Studio 2019/2022 developer command prompt.

2. We're going to compile for 64 bit by executing the following command:

    ```bash 
    "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x64
    ```

    <small>Change the path to your Visual Studio path</small>

3. Now we need to put Tcl on our path. Run the following:

    ```bash
    SET PATH=%PATH%;C:\ActiveTcl\bin
    ```

4. Set the platform which we want to build sqlite for.

    ```bash
    SET PLATFORM=x64
    ```

#### Download sqlcipher

Clone the repository of sqlcipher into a folder.

```bash
git clone https://github.com/sqlcipher/sqlcipher.git D:\Temp\Github\sqlcipher
```

Change the `D:\Temp\Github\sqlcipher` to any path you like (ex: `C:\Cloned\sqlcipher`)

#### Fixing the Makefile

Since we're compiling for Windows, we need to fix the `Makefile.msc` located in the root of the repository with the following:

1. Find the string -DSQLITE_TEMP_STORE=1 and change 1 to 2. You should change it in 2 places the TCC and RCC variables. Once you've changed those, add the following right below

```bash
# Flags to include OpenSSL
TCC = $(TCC) -DSQLITE_HAS_CODEC -I"C:\Program Files\OpenSSL-Win64\include"
```
where `C:\Program Files\OpenSSL-Win64\include` is the folder where you installed OpenSSL.

2. Locate the string `LTLIBPATHS = $(LTLIBPATHS) /LIBPATH:$(ICULIBDIR)` right after the `!ENDIF`, add the following:

```bash
LTLIBPATHS = $(LTLIBPATHS) /LIBPATH:$(ICULIBDIR) /LIBPATH:"C:\Program Files\OpenSSL-Win64\lib\VC\static"
LTLIBS = $(LTLIBS) libcrypto64MT.lib libssl64MT.lib ws2_32.lib shell32.lib advapi32.lib gdi32.lib user32.lib crypt32.lib kernel32.lib
```

#### Create binary folder

Create a folder where you want the binaries to be built. I chose to create a folder at the same level as the cloned repository, located at `D:\Temp\GitHub\sqlcipher-build`

#### Compiling

In your binary folder ( `cd D:\Temp\GitHub\sqlcipher-build`), run the following:

```bash
nmake /f D:\Temp\GitHub\sqlcipher\Makefile.msc TOP=D:\Temp\GitHub\sqlcipher
```

Replace the folders with your appropriate folders. You should now find sqlite3.exe and sqlite3.dll in the directory.

#### Add to path
Add `sqlcipher-build` folder to system environment variables and restart your PC.

## Run
Give permission to execute runner by using:
```bash
chmod +x runner.sh
```

### Usage
```
usage: ./runner.sh [-y] [-h] [-t [CLIPBOARD_TTL]] [-p [HIDE_SECRET_TTL]]
             [-a [AUTO_LOCK_TTL]] [-v VAULT_LOCATION] [-c CONFIG_LOCATION]
             [-k] [-i IMPORT_ITEMS] [-x EXPORT] [-f [{json}]] [-e]

optional arguments:
  --help                show this help message and exit
  -t [CLIPBOARD_TTL], --clipboard_TTL [CLIPBOARD_TTL]
                        Set clipboard TTL (in seconds, default: 15)
  -p [HIDE_SECRET_TTL], --hide_secret_TTL [HIDE_SECRET_TTL]
                        Set delay before hiding a printed password (in
                        seconds, default: 15)
  -a [AUTO_LOCK_TTL], --auto_lock_TTL [AUTO_LOCK_TTL]
                        Set auto lock TTL (in seconds, default: 900)
  -v VAULT_LOCATION, --vault_location VAULT_LOCATION
                        Set vault path
  -c CONFIG_LOCATION, --config_location CONFIG_LOCATION
                        Set config path
  -k, --change_key      Change master key
  -i IMPORT_FILE, --import_file IMPORT_FILE
                        File to import credentials from
  -x EXPORT_FILE, --export_file EXPORT_FILE
                        File to export credentials to
  -f [{json}], --file_format [{json}]
                        Import/export file format (default: 'json')
  -e, --erase_vault     Erase the vault and config file
```
