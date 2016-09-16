"""
    Wrapper functions for FuncYms
    This functions include Onosclidriver and OnosRestDriver driver functions
    Author: antony.silvester@huawei.com
"""
import os
import pexpect
import shutil
import time

def gitCloneAndBuild( main, path, url, skipTest=True, mciTimeout=600):

    folder = url.split( "/" )[-1].split( "." )[0]
    dest = path + "/" + folder
    
    if os.path.exists( dest ):
        main.log.info( "Removing folder " + dest )
        shutil.rmtree(dest, ignore_errors=True)

    main.log.info( "Cloning git repository" )
    main.ONOSbench.handle.sendline( "cd " + path)
    main.ONOSbench.handle.expect( "\$" )
    
    main.ONOSbench.handle.sendline( "git clone " + url )
    main.ONOSbench.handle.expect( "\$" )

    time.sleep(1)
    
    if os.path.exists(dest):
        main.log.info( "Building " + folder )        
        main.ONOSbench.handle.sendline( "cd " + folder )
        main.ONOSbench.handle.expect( "\$" )
    
        if skipTest:
            main.ONOSbench.handle.sendline( "mvn clean install -DskipTests" +
                                  " -Dcheckstyle.skip -U -T 1C" )
        else:
            main.ONOSbench.handle.sendline( "mvn clean install" )            
    
        i = main.ONOSbench.handle.expect( [
            'There\sis\sinsufficient\smemory\sfor\sthe\sJava\s' +
            'Runtime\sEnvironment\sto\scontinue',
            'BUILD\sFAILURE',
            'BUILD\sSUCCESS',
            'onos\$',  #TODO: fix this to be more generic?
            'ONOS\$',
            pexpect.TIMEOUT ], mciTimeout )
        if i == 0:
            main.log.error( "There is insufficient memory \
                    for the Java Runtime Environment to continue." )
        if i == 1:
            main.log.error( "Build failure!" )
        elif i == 2:
            main.log.info( "Build success!" )
        elif i == 3 or i == 4:
            main.log.info( "Build complete" )
        elif i == 5:
            main.log.error( "mvn clean install TIMEOUT!" )
        else:
            main.log.error( "Unexpected response from " +
                            "mvn clean install" )
    else:
        main.log.error( "Cloning git repository failed! " )  
    
