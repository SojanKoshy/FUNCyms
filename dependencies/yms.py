import pexpect

def gitClone( self, path, url):
    main.ONOSbench.handle.sendline("cd " + path)
    main.ONOSbench.handle.expect( "\$" )
    main.ONOSbench.handle.sendline("git clone " + url)
    main.ONOSbench.handle.expect( "\$" )

def mvnCleanInstall( self, path, folder, skipTest=True, mciTimeout=600):
    main.ONOSbench.handle.sendline("cd " + path + '\\' + folder)
    main.ONOSbench.handle.expect( "\$" )

    if skipTest:
        main.ONOSbench.handle.sendline( "mvn clean install -DskipTests" +
                              " -Dcheckstyle.skip -U -T 1C" )
    else:
        main.ONOSbench.handle.sendline( "mvn clean install" )

    main.ONOSbench.handle.expect( [
                'There\sis\sinsufficient\smemory\sfor\sthe\sJava\s' +
                'Runtime\sEnvironment\sto\scontinue',
                'BUILD\sFAILURE',
                'BUILD\sSUCCESS',
                folder + '\$',
                pexpect.TIMEOUT ], mciTimeout )
