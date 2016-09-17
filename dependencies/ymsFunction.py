"""
    Wrapper functions for FuncYms
    This functions include Onosclidriver and OnosRestDriver driver functions
    Author: antony.silvester@huawei.com
"""
import os
import pexpect
import time

def gitCloneAndBuild( main, path, url, forceBuild=False ):
    """
    Clones the git url or do git pull.
    Runs mvn clean install in the newly created or pulled directory.
    Returns: main.TRUE on success
    On Failure, exits the test
    """

    folder = url.split( "/" )[-1].split( "." )[0]
    dest = path + "/" + folder

    oldHome = main.ONOSbench.home

    main.ONOSbench.handle.sendline( "cd " + path )
    main.ONOSbench.handle.expect( "cd " )
    main.ONOSbench.handle.expect( "\$" )

    buildRequired = forceBuild

    if not os.path.exists( dest ):
        main.log.info( "Cloning git repository" )
        buildRequired = True
        main.ONOSbench.handle.sendline( "git clone " + url )
        main.ONOSbench.handle.expect( "git clone " + url )
        main.ONOSbench.handle.expect( "\$" )

        time.sleep( 1 )

        if not os.path.exists( dest ):
            main.log.error( "Cloning git repository failed! " )
            main.cleanup()
            main.exit()
    else:
        if os.path.exists( dest + "/.git" ):
            main.log.info( "Pulling latest code from github" )

            main.ONOSbench.home = folder
            pullResult = main.ONOSbench.gitPull()
            if pullResult == main.TRUE:
                buildRequired = True
            main.ONOSbench.home = oldHome
        else:
            main.log.warn( "Skipping git pull since folder is already "
                           + "present and is not git clone" )
    if buildRequired:
        main.ONOSbench.handle.sendline( "cd " + path )
        main.ONOSbench.handle.expect( "cd " )
        main.ONOSbench.handle.expect( "\$" )

        cleanInstall( main, folder )
    else:
        main.log.warn( "Did not pull new code so skipping mvn clean install" )

    main.ONOSbench.handle.sendline( "cd " + main.ONOSbench.home )
    return main.TRUE

def cleanInstall( main, folder, skipTest=True, mciTimeout=300 ):
    """
    Runs mvn clean install in the directory specified.
    This will clean all artifacts then compile each module
    Optional:
        skipTest - Does "-DskipTests -Dcheckstyle.skip -U -T 1C" which
                   skip the test. This will make the building faster.
                   Disregarding the credibility of the build
    Returns: main.TRUE on success
    On Failure, exits the test
    """
    try:
        main.log.info( "Running 'mvn clean install' on " +
                       folder +
                       ". This may take some time." )
        main.ONOSbench.handle.sendline( "cd " + folder )
        main.ONOSbench.handle.expect( "cd " + folder )
        main.ONOSbench.handle.expect( "\$" )

        main.ONOSbench.handle.sendline( "" )
        main.ONOSbench.handle.expect( "\$" )

        if not skipTest:
            main.ONOSbench.handle.sendline( "mvn clean install" )
            main.ONOSbench.handle.expect( "mvn clean install" )
        else:
            main.ONOSbench.handle.sendline( "mvn clean install -DskipTests" +
                                  " -Dcheckstyle.skip -U -T 1C" )
            main.ONOSbench.handle.expect( "mvn clean install -DskipTests" +
                                  " -Dcheckstyle.skip -U -T 1C" )
        while True:
            i = main.ONOSbench.handle.expect( [
                'There\sis\sinsufficient\smemory\sfor\sthe\sJava\s' +
                'Runtime\sEnvironment\sto\scontinue',
                'BUILD\sFAILURE',
                'BUILD\sSUCCESS',
                folder + '\$',
                pexpect.TIMEOUT ], mciTimeout )
            if i == 0:
                main.log.error( "There is insufficient memory \
                        for the Java Runtime Environment to continue." )
                main.cleanup()
                main.exit()
            if i == 1:
                main.log.error( "Build failure!" )
                main.cleanup()
                main.exit()
            elif i == 2:
                main.log.info( "Build success!" )
            elif i == 3:
                main.log.info( "Build complete" )
                # Print the build time
                for line in main.ONOSbench.handle.before.splitlines():
                    if "Total time:" in line:
                        main.log.info( line )
                main.ONOSbench.handle.sendline( "" )
                main.ONOSbench.handle.expect( "\$", timeout=60 )
                return main.TRUE
            elif i == 4:
                main.log.error( "mvn clean install TIMEOUT!" )
                main.cleanup()
                main.exit()
            else:
                main.log.error( "Unexpected response from " +
                                "mvn clean install" )
                main.cleanup()
                main.exit()
    except pexpect.EOF:
        main.log.error( "EOF exception found" )
        main.log.error( "     " + main.ONOSbench.handle.before )
        main.cleanup()
        main.exit()
    except Exception:
        main.log.exception( "Uncaught exception!" )
        main.cleanup()
        main.exit()
