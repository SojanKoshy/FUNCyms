"""
    Wrapper functions for FuncYms
    This functions include Onosclidriver and OnosRestDriver driver functions
    Author: antony.silvester@huawei.com
"""
import pexpect
import shutil

def gitCloneAndBuild( main, path, url, skipTest=True, mciTimeout=600):

    # Delete destination folder if present
    folder = url.split("/")[-1].split(".")[0]
    dest = path + '\\' + folder
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)

    # Clone git reprository
    main.ONOSbench.handle.sendline("cd " + path)
    main.ONOSbench.handle.expect( "\$" )
    main.ONOSbench.handle.sendline("git clone " + url)
    main.ONOSbench.handle.expect( "\$" )

    # Maven clean build
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
