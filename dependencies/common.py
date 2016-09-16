import pexpect

class Common:

    def mvnCleanInstall( self, folder, skipTest=True, mciTimeout=600):
        main.ONOSbench.handle.sendline("cd " + folder)
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